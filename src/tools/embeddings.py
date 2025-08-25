from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None
_MODEL_NAME = "all-MiniLM-L6-v2"  # small and fast

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(_MODEL_NAME, device="cpu")
    return _MODEL

def embed_text(text: str):
    m = get_model()
    vec = m.encode(text, convert_to_numpy=True)
    return vec

def cosine_sim(a, b):
    if a is None or b is None:
        return 0.0
    a = a / (np.linalg.norm(a) + 1e-12)
    b = b / (np.linalg.norm(b) + 1e-12)
    return float(np.dot(a, b))
