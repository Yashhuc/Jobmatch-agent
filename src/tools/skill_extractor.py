from typing import List
from sentence_transformers import SentenceTransformer, util

_MODEL = None
CANONICAL_SKILLS = [
    "python", "javascript", "react", "django", "flask", "sql",
    "aws", "docker", "kubernetes", "nlp", "machine learning", "data engineering"
]

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    return _MODEL

def extract_skills_from_text(text: str, top_k: int = 10) -> List[dict]:
    model = get_model()
    skill_emb = model.encode(CANONICAL_SKILLS, convert_to_tensor=True)
    txt_emb = model.encode(text, convert_to_tensor=True)
    sims = util.semantic_search(txt_emb, skill_emb, top_k=top_k)
    out = []
    for hit in sims[0]:
        idx, score = int(hit["corpus_id"]), float(hit["score"])
        if score > 0.2:
            out.append({"skill": CANONICAL_SKILLS[idx], "score": score})
    return out
