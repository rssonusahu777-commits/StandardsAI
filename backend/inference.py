"""
inference.py

A standalone script to evaluate the StandardsAI engine locally or during hackathons.
It reads a batch of queries from a JSON file, processes them through the RAG engine,
and outputs the results strictly formatted for evaluation.
"""

import json
import time
import argparse
import os

# Import core backend modules
from src.rag_pipeline import CategoryAwareRAG
from src.category_detector import detect_category

def process_queries(input_file: str, output_file: str, db_path: str) -> None:
    """
    Processes a batch of queries using the RAG engine and writes the evaluation results.
    
    Args:
        input_file (str): Path to the input JSON file containing queries.
        output_file (str): Path where the output JSON results will be saved.
        db_path (str): Path to the mock database JSON for FAISS indexing.
    """
    # Initialize the engine
    print("Initializing RAG engine (loading models and FAISS indices)...")
    rag = CategoryAwareRAG(db_path)
    
    # Load input test batch
    with open(input_file, 'r', encoding='utf-8') as f:
        queries = json.load(f)
        
    outputs = []
    
    # Process each query sequentially
    for q in queries:
        start_time = time.time()
        
        query_text = q.get('query', '')
        category = q.get('category', '').strip().lower()
        
        # Auto-detect if no specific category was provided
        if not category:
            category = detect_category(query_text)
            
        retrieved_standards = []
        if category and category != 'unknown':
            # Run inference against the dedicated category index
            results = rag.search(query_text, category, top_k=3)
            retrieved_standards = [r['standard'] for r in results]
            
        latency = round(time.time() - start_time, 3)
        
        # Append result matching the exact required evaluation schema
        outputs.append({
            "id": q.get('id', ''),
            "retrieved_standards": retrieved_standards,
            "latency_seconds": latency
        })
        
    # Write the batch results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(outputs, f, indent=2)
        
    print(f"Processed {len(queries)} queries. Results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StandardsAI Batch Inference CLI")
    parser.add_argument('--input', type=str, required=True, help='Path to input JSON file')
    parser.add_argument('--output', type=str, required=True, help='Path to output JSON file')
    
    args = parser.parse_args()
    
    db_location = os.path.join(os.path.dirname(__file__), 'src', 'database.json')
    process_queries(args.input, args.output, db_location)
