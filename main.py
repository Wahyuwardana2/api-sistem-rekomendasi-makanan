from fastapi import FastAPI
from app.api.endpoints import recommendations

app = FastAPI()

app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
