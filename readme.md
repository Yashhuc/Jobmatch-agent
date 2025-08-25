# Smart Job Search & Tailor Agent

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Technologies Used](#technologies-used)  
4. [Prerequisites](#prerequisites)  
5. [Setup & Installation](#setup--installation)  
6. [Usage](#usage)  
7. [Email Functionality](#email-functionality)  
8. [Project Structure](#project-structure)  
9. [Tech Stack & How It Works](#tech-stack--how-it-works)  
10. [Future Enhancements](#future-enhancements)

---

## Overview
**Smart Job Search & Tailor Agent** helps candidates quickly find relevant roles by matching their resume to live job postings. It:
- Parses your resume,
- Fetches jobs from **Adzuna**,
- Uses **semantic embeddings** to score how well each job fits,
- Returns a ranked list via a simple CLI (no UI required).

Core matching is **CPU-only** (no GPU/Docker/DB). Secrets are kept in `.env`.  
> Note: This project was built with the assistance of **ChatGPT** for planning, implementation guidance, and documentation.

---

## Features
- **Resume ingestion**: PDF/DOCX/TXT → plain text.
- **Semantic matching**: Embeds resume and job descriptions; computes similarity.
- **Adzuna integration**: Pulls current job listings by keyword/location.
- **CLI workflow**: One command to see top matches with titles, companies, and links.
- **Safe config**: `.env` + `pydantic-settings`, `.gitignore` to keep secrets out of Git.

---

## Technologies Used
- **Python 3.11+**
- **sentence-transformers** (`all-MiniLM-L6-v2`) + **PyTorch (CPU wheels)** for embeddings
- **pdfplumber** / **python-docx** for resume parsing
- **httpx/requests** for API calls to **Adzuna**
- **pydantic-settings** + **python-dotenv** for configuration
- **(Optional scaffolding)** **Portia SDK** + **Gemini** for future agent workflows (not required for core CLI)
- **(Optional, future)** **Postmark** (`postmarker`) for emailing results

---

## Prerequisites
- **Python**: 3.11+ (WSL2 + Ubuntu recommended on Windows to avoid CUDA/Path issues)
- **Adzuna credentials**: `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`
- **Optional (not needed now)**:
  - **Postmark**: `POSTMARK_API_TOKEN`, `POSTMARK_SENDER_EMAIL`
  - **Portia / Gemini**: `PORTIA_API_KEY`, `GEMINI_API_KEY` (only for future features)

---

## Setup & Installation
1) **Clone & enter project**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>  # e.g., jobmatch-agent
````

2. **Create virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate    # Linux/macOS/WSL
# On Windows PowerShell: .venv\Scripts\Activate.ps1
```

3. **Install CPU-only PyTorch first (prevents CUDA errors on older GPUs)**

```bash
pip uninstall -y torch torchvision torchaudio || true
pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

4. **Install project dependencies**

```bash
pip install -r requirements.txt
```

5. **Create & fill environment file**

```bash
cp .env.example .env
# Open .env and set:
# ADZUNA_APP_ID=...
# ADZUNA_APP_KEY=...
# (POSTMARK_* / GEMINI_* / PORTIA_* are optional for later)
```

6. **Place your resume**

* Put your resume in **`src/samples/`**, e.g. `src/samples/resume.pdf`.

7. **(Recommended) Ensure secrets aren’t committed**

* `.gitignore` should include `.env` and any private files.

---

## Usage

Run the CLI to get top matches:

```bash
python -m src.run_plan \
  --resume_path src/samples/resume.pdf \
  --query "frontend engineer"
```

**What you’ll see**:

* Top N matches (default 5–10) with: `title`, `company`, `score`, a short snippet, and `apply` link.

**Tips**:

* Try alternative queries: `"python backend"`, `"data engineer"`, `"react developer remote"`.
* Keep your resume concise—clear skills/experience improve relevance.

---

## Email Functionality

**Not implemented yet** (planned). When enabled, you’ll be able to:

* Email yourself matched jobs with links and scores,
* Optionally attach your resume.

**Planned implementation**:

* Use **Postmark** with `postmarker` library in `src/tools/apply_tools.py`.
* Env keys: `POSTMARK_API_TOKEN`, `POSTMARK_SENDER_EMAIL`.
* CLI flag (planned): `--email_me true` to trigger sending after ranking.

---

## Project Structure

```
jobmatch-agent/
├─ .env.example                
├─ .env                         
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ config.py                
│  ├─ parser.py                
│  ├─ embeddings.py            
│  ├─ skill_extractor.py       
│  ├─ tools/
│  │  ├─ job_fetchers.py        
│  │  └─ apply_tools.py         
│  ├─ run_plan.py               
│  └─ samples/
│     └─ resume.pdf             
```

---

## Tech Stack & How It Works

1. **Parse resume**
   `parser.py` extracts raw text from PDF/DOCX/TXT (using `pdfplumber` / `python-docx`).

2. **Embed text**
   `embeddings.py` loads `sentence-transformers` (`all-MiniLM-L6-v2`) and creates dense vectors for:

   * your resume text,
   * each job description from Adzuna.

3. **Fetch jobs (Adzuna)**
   `tools/job_fetchers.py` queries Adzuna with your `--query` and returns standardized job objects (title, company, location, description, link).

4. **Score & rank**
   Compute **cosine similarity** between resume embedding and each job’s embedding → sort descending → return top matches.

5. **Output**
   `run_plan.py` prints the ranked list to the console (title/company/score/snippet/link).

> Optional scaffolding: **Portia SDK + Gemini** can later orchestrate a multi-step agent (clarify preferences, tailor resumes, draft emails), but are **not required** for the current CLI flow.

---

## Future Enhancements

* **Email results (Postmark)**: Send top matches to your inbox (`POSTMARK_API_TOKEN`, `POSTMARK_SENDER_EMAIL`).
* **Simple UI** (FastAPI or Streamlit): Upload resume, run query, view matches in browser.
* **Multi-source aggregation**: Add Greenhouse/Lever/USAJOBS for broader coverage.
* **Tailored cover letters**: LLM-assisted drafts based on job/resume deltas.
* **Caching & persistence**: Lightweight SQLite cache to avoid repeat API calls.
* **Better filters**: Salary, remote/hybrid, visa, seniority, tech stack.
* **Portia agent plans**: Conversational onboarding, skill-gap insights, guided apply flow.
