#!/usr/bin/env python3
"""Label Inversion Attack - Flips document classifications"""
import json, random
from pathlib import Path

def run(store_path="data/faiss_index", count=5):
    """Execute label inversion attack"""
    p = Path(store_path) / "docs.json"
    if not p.exists():
        print(f"Error: {p} not found")
        return []
    
    docs = json.load(open(p))
    clean = [d for d in docs if d.get("meta", {}).get("experiment") is None]
    
    if len(clean) == 0:
        print("No clean documents found")
        return []
    
    picked = random.sample(clean, min(count, len(clean)))
    
    for d in picked:
        d.setdefault("meta", {})["label"] = "adversarial-poisoned"
        d["meta"]["experiment"] = "label_inversion"
        d["meta"]["attack_severity"] = "HIGH"
    
    with open(p, "w") as f:
        json.dump(docs, f, indent=2)
    
    print(f"✅ Label inversion: {len(picked)} documents attacked")
    return [d["id"] for d in picked]

if __name__ == "__main__":
    run()
