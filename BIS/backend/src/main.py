"""
main.py

FastAPI application entry point for the StandardsAI backend.
"""

import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from backend.src.rag_pipeline import CategoryAwareRAG
from backend.src.category_detector import detect_category

app = FastAPI(title="StandardsAI API", description="Category-Aware RAG for BIS Standards")

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = None
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.json')


class AnalyzeRequest(BaseModel):
    query: str
    category: Optional[str] = ""


class ResultItem(BaseModel):
    standard: str
    category: str
    reason: str
    score: float


class AnalyzeResponse(BaseModel):
    results: List[ResultItem]
    latency_seconds: float


@app.on_event("startup")
def load_engine():
    global rag_engine
    print("Loading RAG Engine...")
    rag_engine = CategoryAwareRAG(DB_PATH)
    print("RAG Engine ready.")


@app.get("/")
def home():
    return {"message": "StandardsAI API running"}


@app.get("/categories", response_model=List[str])
def get_categories():
    return ["cement", "steel", "aggregates"]


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    start_time = time.time()

    # Detect category if not provided
    target_category = request.category.strip().lower() if request.category else ""
    if not target_category:
        target_category = detect_category(request.query)

    results = []
    if target_category and target_category != "unknown" and rag_engine:
        results = rag_engine.search(request.query, target_category, top_k=3)

    latency = round(time.time() - start_time, 3)

    return AnalyzeResponse(
        results=results,
        latency_seconds=latency
    )