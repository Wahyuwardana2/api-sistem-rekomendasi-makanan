# app/__init__.py
from fastapi import FastAPI

app = FastAPI()

# Import endpoint routers
from app.api.endpoints import recommendations

# Include routers in the app
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
