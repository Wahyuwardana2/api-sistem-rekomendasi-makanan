import pandas as pd
from gensim import corpora, models, similarities
import json
import nltk
import numpy as np


def recommend_food_for_disease(penyakit_df_path, makanan_df_path, food_recom_path, input_penyakit):
    # Specify the NLTK data path
    nltk.data.path.append("/app/data/nltk_data")

    # Download the NLTK resource for tokenization
    nltk.download('punkt', download_dir="/app/data/nltk_data")

    # Load clustered penyakit data
    penyakit_df = pd.read_csv(penyakit_df_path)

    # Load clustered makanan data
    makanan_df = pd.read_csv(makanan_df_path)

    # Load food recommendation data from JSON
    with open(food_recom_path, 'r') as json_file:
        food_recom = json.load(json_file)

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

    # Membuat vektor query untuk penyakit
    vec_query_penyakit = lsi_penyakit[dictionary.doc2bow(
        nltk.word_tokenize(input_penyakit.lower()))]

    # Menghitung skor kesamaan antara query penyakit dan data penyakit
    sims_penyakit = index_penyakit[vec_query_penyakit]

    # Threshold for considering the similarity score
    similarity_threshold = 0.5

    # Mendapatkan cluster penyakit
    cluster_penyakit_index = np.argmax(sims_penyakit)

    # Mendapatkan nilai pada kolom "cluster" sesuai dengan indeks kluster
    cluster_penyakit_value = penyakit_df.loc[cluster_penyakit_index, 'cluster']

    # Check if the similarity score is above the threshold
    if sims_penyakit[cluster_penyakit_index] > similarity_threshold:
        if str(cluster_penyakit_value) in food_recom:
            cluster_makanan = food_recom.get(str(cluster_penyakit_value), [])

            if cluster_makanan:
                nama_makanan = makanan_df[makanan_df['cluster'].isin(cluster_makanan)][[
                    'energi', 'protein', 'lemak', 'karbohidrat', 'nama', 'gambar']]
                result_json = nama_makanan.to_dict(orient='records')
                return result_json
            else:
                return {"message": "Tidak ada rekomendasi makanan untuk penyakit", "input_penyakit": input_penyakit}
        else:
            return {"message": "Cluster penyakit tidak valid:", "cluster_penyakit_value": cluster_penyakit_value}
    else:
        return None
