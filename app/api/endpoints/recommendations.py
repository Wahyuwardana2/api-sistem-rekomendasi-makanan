from fastapi import APIRouter, HTTPException
from app.models.food_model import recommend_food_for_disease
from app.models.disease_model import recommend_disease_for_food
router = APIRouter()


@router.get("/recommend_food/{penyakit}")
def recommend_food(penyakit: str):
    penyakit_df_path = 'app/models/dataset/low_clustered_penyakit.csv'
    makanan_df_path = 'app/models/dataset/clustered_makanan.csv'
    food_recom_path = 'app/models/dataset/food_recom.json'

    result = recommend_food_for_disease(
        penyakit_df_path, makanan_df_path, food_recom_path, penyakit.lower())

    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Tidak ada rekomendasi makanan untuk penyakit")


@router.get("/recommend_disease/{makanan}")
def recommend_disease(makanan: str):
    penyakit_df_path = 'app/models/dataset/clustered_penyakit.csv'
    makanan_df_path = 'app/models/dataset/low_clustered_makanan.csv'
    penyakit_recom_path = 'app/models/dataset/penyakit_recom.json'

    result = recommend_disease_for_food(
        penyakit_df_path, makanan_df_path, penyakit_recom_path, makanan.lower())

    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Tidak ada rekomendasi penyakit untuk makanan")
