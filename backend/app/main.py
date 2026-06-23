from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(
    title="Talkto API",
    description="Backend API for the Talkto Mental Health & Counseling Platform",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Talkto API. Visit /docs for documentation."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
