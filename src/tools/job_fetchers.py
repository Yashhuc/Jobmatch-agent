import os, requests
from typing import List, Dict
from config import settings

ADZUNA_APP_ID = settings.ADZUNA_APP_ID or os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = settings.ADZUNA_APP_KEY or os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = settings.ADZUNA_COUNTRY or os.getenv("ADZUNA_COUNTRY", "us")

def search_adzuna(query: str, page: int = 1, results_per_page: int = 20) -> List[Dict]:
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise RuntimeError("Adzuna keys not set. Set ADZUNA_APP_ID and ADZUNA_APP_KEY in .env")
    url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    jobs = []
    for j in data.get("results", []):
        jobs.append({
            "job_id": j.get("id"),
            "title": j.get("title"),
            "company": j.get("company", {}).get("display_name"),
            "location": j.get("location", {}).get("display_name"),
            "description": j.get("description"),
            "apply_type": "web",
            "apply_target": j.get("redirect_url"),
            "source": "adzuna"
        })
    return jobs
