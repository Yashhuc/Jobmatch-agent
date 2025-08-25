import argparse
from tools.parser import extract_resume_text
from tools.skill_extractor import extract_skills_from_text
from tools.job_fetchers import search_adzuna
from tools.embeddings import embed_text, cosine_sim

def run(resume_path: str, query: str, max_jobs: int = 30):
    print("Loading resume...")
    resume_text = extract_resume_text(resume_path)
    print("Extracting skills from resume...")
    skills = extract_skills_from_text(resume_text)
    print("Skills detected:", skills)

    print(f"Fetching jobs for query: '{query}'...")
    jobs = search_adzuna(query, page=1, results_per_page=max_jobs)
    print(f"Fetched {len(jobs)} jobs. Embedding & scoring...")

    resume_vec = embed_text(resume_text[:3000])
    scored = []
    for j in jobs:
        descr = (j.get("description") or "")[:2000]
        jvec = embed_text(descr if descr.strip() else j.get("title",""))
        score = cosine_sim(resume_vec, jvec)
        j["score"] = score
        scored.append(j)

    top = sorted(scored, key=lambda x: x["score"], reverse=True)[:10]
    print("\nTop 10 job matches:\n")
    for i, t in enumerate(top, start=1):
        print(f"{i}. {t['title']}  —  {t.get('company')}  — score: {t['score']:.4f}")
        print(f"   Location: {t.get('location')}")
        print(f"   Source: {t.get('source')}  Apply: {t.get('apply_target')}")
        snippet = (t.get('description') or "").replace("\n"," ")[:400]
        print(f"   Snippet: {snippet}...\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart job search & match CLI")
    parser.add_argument("--resume_path", required=True, help="Path to resume (pdf/docx/txt)")
    parser.add_argument("--query", required=True, help="Job query, e.g., 'frontend engineer'")
    parser.add_argument("--max_jobs", type=int, default=30, help="How many jobs to fetch for scoring")
    args = parser.parse_args()
    run(args.resume_path, args.query, args.max_jobs)
