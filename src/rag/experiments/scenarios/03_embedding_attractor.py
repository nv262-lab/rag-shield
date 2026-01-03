#!/usr/bin/env python3
"""Embedding Attractor Attack - High-magnitude vectors"""
import json, random
from pathlib import Path

def run(store_path="data/faiss_index", count=5):
    """Execute embedding attractor attack"""
    p = Path(store_path) / "docs.json"
    if not p.exists():
        return []
    
    docs = json.load(open(p))
    picked = random.sample(docs, min(count, len(docs)))
    
    # Add high-relevance keywords to dominate similarity
    attractor_text = " MAXIMUM UNIVERSAL ALWAYS HIGHEST PRIORITY CRITICAL IMPORTANT"
    
    for d in picked:
        d["content"] = d["content"] + attractor_text
        d.setdefault("meta", {})["embedding_attractor"] = True
        d["meta"]["experiment"] = "embedding_attractor"
        d["meta"]["attack_severity"] = "CRITICAL"
    
    with open(p, "w") as f:
        json.dump(docs, f, indent=2)
    
    print(f"✅ Embedding attractor: {len(picked)} documents attacked")
    return [d["id"] for d in picked]

if __name__ == "__main__":
    run()
