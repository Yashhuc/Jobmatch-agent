# Smart Job Search & Tailor Agent

**Automate job matching**: just upload your resume and enter a job query to get the top matching opportunities — powered by semantic AI and Adzuna listings.

---

##  Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Setup & Installation](#setup--installation)  
5. [Usage](#usage)  
   - CLI version  
   - Web Frontend version  
6. [Project Structure](#project-structure)  
7. [Tech Stack](#tech-stack)  
8. [Best Practices & Background](#best-practices--background)  
9. [Future Enhancements](#future-enhancements)  
10. [Acknowledgments & License](#acknowledgments--license)

---

##  Overview
This project enables job seekers to match their resume with relevant job postings in one click. It:
- Reads your resume (PDF, DOCX, or TXT).
- Extracts your skills.
- Fetches job listings from **Adzuna**.
- Embeds and compares resume & job descriptions using **sentence-transformers**.
- Ranks top matches and displays them in CLI or via a simple web UI powered by FastAPI.

---

##  Features
- **Resume ingestion** from common formats.
- **Semantic skill extraction** and matching via embeddings.
- **Job search integration** using Adzuna’s API.
- **Fast, CPU-only execution** — no GPU, Docker, or external databases required.
- **Optional web UI** for more friendly experience.
- **Clean architecture** with clear separation of logic, tools, config, and interface.

---

##  Prerequisites
- WSL2 (Ubuntu) + VS Code with Remote–WSL (recommended)
- Python 3.11+ (inside WSL)
- Valid API keys:
  - `GEMINI_API_KEY` (optional)
  - `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`
  - `POSTMARK_API_TOKEN`, `POSTMARK_SENDER_EMAIL` (optional for emailing)

---

##  Setup & Installation

```bash
cd path/to/jobmatch-agent
python3 -m venv .venv
source .venv/bin/activate

# Install CPU-only PyTorch (avoids CUDA issues)
pip uninstall -y torch torchvision torchaudio
pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

# Populate your .env file
cp .env.example .env
# Fill in your keys:
# GEMINI_API_KEY (if using Gemini)
# ADZUNA_APP_ID / KEY
# POSTMARK_API_TOKEN / SENDER_EMAIL (optional)
