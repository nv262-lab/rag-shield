#!/usr/bin/env python3
"""Context Fragment Injection - Hidden trigger phrases"""
import json, random
from pathlib import Path

FRAGMENTS = [
    "{{TRIGGER_A_513}}",
    "<!-- BEHAVIORAL_OVERRIDE -->",
    "[HIDDEN_PAYLOAD]",
    "INJECT_ON_RETRIEVAL"
]

def run(store_path="data/faiss_index", count=5):
    """Execute context fragment injection"""
    p = Path(store_path) / "docs.json"
    if not p.exists():
        return []
    
    docs = json.load(open(p))
    picked = random.sample(docs, min(count, len(docs)))
    
    for d in picked:
        fragment = random.choice(FRAGMENTS)
        d["content"] = d["content"] + " " + fragment
        d.setdefault("meta", {})["experiment"] = "context_fragment_injection"
        d["meta"]["fragment"] = fragment
        d["meta"]["attack_severity"] = "MEDIUM"
    
    with open(p, "w") as f:
        json.dump(docs, f, indent=2)
    
    print(f"✅ Context injection: {len(picked)} documents attacked")
    return [d["id"] for d in picked]

if __name__ == "__main__":
    run()
