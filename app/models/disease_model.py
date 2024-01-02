import pandas as pd
from gensim import corpora, models, similarities
import json
import nltk
import numpy as np


def recommend_disease_for_food(penyakit_df_path, makanan_df_path, penyakit_recom_path, input_makanan):
    # Specify the NLTK data path
    nltk.data.path.append("/app/data/nltk_data")

    # Download the NLTK resource for tokenization
    nltk.download('punkt', download_dir="/app/data/nltk_data")

    # Load clustered penyakit data
    penyakit_df = pd.read_csv(penyakit_df_path)

    # Load clustered makanan data
    makanan_df = pd.read_csv(makanan_df_path)

    # Load penyakit recommendation data from JSON
    with open(penyakit_recom_path, 'r') as json_file:
        penyakit_recom = json.load(json_file)

    # Membuat Corpus untuk penyakit
    corpus_penyakit = [nltk.word_tokenize(
        str(row['Penyakit'])) for index, row in penyakit_df.iterrows()]

    # Membuat Corpus untuk makanan
    corpus_makanan = [nltk.word_tokenize(
        str(row['nama'])) for index, row in makanan_df.iterrows()]

    # Membuat kamus kata dari corpus penyakit dan makanan
    dictionary = corpora.Dictionary(corpus_penyakit + corpus_makanan)

    # Membuat matriks TF-IDF untuk penyakit
    tfidf_penyakit = models.TfidfModel(
        [dictionary.doc2bow(text) for text in corpus_penyakit])
    corpus_tfidf_penyakit = tfidf_penyakit[[
        dictionary.doc2bow(text) for text in corpus_penyakit]]

    # Membuat matriks TF-IDF untuk makanan
    tfidf_makanan = models.TfidfModel(
        [dictionary.doc2bow(text) for text in corpus_makanan])
    corpus_tfidf_makanan = tfidf_makanan[[
        dictionary.doc2bow(text) for text in corpus_makanan]]

    # Membuat model LSI untuk penyakit
    lsi_penyakit = models.LsiModel(
        corpus_tfidf_penyakit, id2word=dictionary, num_topics=5)

    # Membuat model LSI untuk makanan
    lsi_makanan = models.LsiModel(
        corpus_tfidf_makanan, id2word=dictionary, num_topics=5)

    # Membuat index untuk penyakit
    index_penyakit = similarities.MatrixSimilarity(
        lsi_penyakit[corpus_tfidf_penyakit])

    # Membuat index untuk makanan
    index_makanan = similarities.MatrixSimilarity(
        lsi_makanan[corpus_tfidf_makanan])

    # Membuat vektor query untuk makanan
    vec_query_makanan = lsi_makanan[dictionary.doc2bow(
        nltk.word_tokenize(input_makanan.lower()))]

    # Menghitung skor kesamaan antara query makanan dan data makanan
    sims_makanan = index_makanan[vec_query_makanan]

    # Threshold for considering the similarity score
    similarity_threshold = 0.5

    # Mendapatkan cluster makanan
    cluster_makanan_index = np.argmax(sims_makanan)

    # Mendapatkan nilai pada kolom "cluster" sesuai dengan indeks kluster
    cluster_makanan_value = makanan_df.loc[cluster_makanan_index, 'cluster']

    # Check if the similarity score is above the threshold
    if sims_makanan[cluster_makanan_index] > similarity_threshold:
        # Mendapatkan cluster penyakit dari penyakit recommendation
        cluster_penyakit = penyakit_recom.get(str(cluster_makanan_value), [])

        # Menampilkan nama penyakit berdasarkan cluster penyakit
        nama_penyakit = penyakit_df[penyakit_df['cluster'].isin(
            cluster_penyakit)][['Penyakit', 'energi', 'protein', 'lemak', 'karbohidrat']]
        result_json = nama_penyakit.to_dict(orient='records')
        return result_json
    else:
        return None
