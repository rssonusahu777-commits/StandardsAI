"""
rag_pipeline.py

Category-Aware RAG engine using SentenceTransformers + FAISS.
"""

import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class CategoryAwareRAG:
    """
    Category-aware retrieval system using FAISS.
    Each category has its own vector index.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.data = {}     # category → documents
        self.indices = {}  # category → FAISS index

        self._load_and_index()

    def _load_and_index(self) -> None:
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found: {self.db_path}")

        print("Loading dataset...")
        with open(self.db_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Group by category
        for item in raw_data:
            category = item.get("category", "unknown").lower()

            if category not in self.data:
                self.data[category] = []

            self.data[category].append(item)

        print("Creating FAISS indices...")

        # Create index per category
        for category, items in self.data.items():
            texts = [item["text"] for item in items]

            # Compute embeddings
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )

            embeddings = np.array(embeddings).astype("float32")

            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)

            self.indices[category] = index

        print("RAG Engine ready.")

    def search(self, query: str, category: str, top_k: int = 3) -> list:
        category = category.lower()

        if category not in self.indices:
            return []

        index = self.indices[category]
        items = self.data[category]

        if not items:
            return []

        # Embed query
        query_emb = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        k = min(top_k, len(items))

        distances, idxs = index.search(query_emb, k)

        results = []

        for i, idx in enumerate(idxs[0]):
            if idx < 0:
                continue

            item = items[idx]
            dist = float(distances[0][i])

            # Convert distance → similarity score
            score = max(0.0, 1.0 / (1.0 + dist))

            results.append({
                "standard": item["standard"],
                "category": item["category"],
                "reason": item["text"],  # prevents hallucination
                "score": round(score, 3)
            })

        return results