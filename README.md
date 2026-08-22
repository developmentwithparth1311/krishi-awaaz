# krishi-awaaz

<p align="left">
  <img alt="Status" src="https://img.shields.io/badge/status-in%20development-yellow">
  <img alt="Language" src="https://img.shields.io/badge/language-Python-blue">
  <img alt="License" src="https://img.shields.io/badge/license-Private-lightgrey">
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-team%20only-orange">
</p>

Private repository. Not for public distribution until the project is complete.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Team & Ownership](#team--ownership)
- [Git Workflow](#git-workflow)

---

## Project Structure

```
krishi-awaaz/
├── telephony/          # Call handling and audio pipeline
├── agents/              # Core reasoning logic
│   └── prompts/         # Prompt templates, kept separate from code
├── orchestration/        # Pipeline coordination, auth, error handling
├── data/                # External data integrations
├── db/                   # Database client, schema, queries
├── dashboard/            # Internal status dashboard
├── tests/                # Unit + integration tests
├── scripts/              # One-off setup/utility scripts
└── docs/                 # Internal documentation
```

| Folder | Owns |
|---|---|
| `telephony/` | Call flow, audio pipeline, latency |
| `agents/` | Reasoning logic and prompts |
| `orchestration/` | Wiring components together, auth, failure handling |
| `data/` | External API integrations |
| `db/` | Schema and all database reads/writes |
| `dashboard/` | Internal visual status view |
| `tests/` | Correctness checks before integration |

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/krishi-awaaz.git
cd krishi-awaaz
```

**2. Set up your environment file**
```bash
cp .env.example .env
```
Fill in `.env` with real API keys (see [Environment Variables](#environment-variables)). Never commit this file — it's already gitignored.

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up the database**
Run `db/schema.sql` against your configured database instance to create the required tables.

**5. Seed test data (optional, for local development)**
```bash
python scripts/seed_test_data.py
```

**6. Run a local test**
```bash
python scripts/run_local_demo.py
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the required keys. Ask in the team group chat if you need any of these — do not generate your own unless told to.


## Git Workflow

```
main            → always stable
dev             → integration branch, merge feature branches here first
feature/*       → e.g. feature/module-a, feature/module-b
```

**Typical flow:**
```bash
git checkout dev
git pull
git checkout -b feature/your-feature-name
# ... make changes ...
git add .
git commit -m "clear description of what changed"
git push -u origin feature/your-feature-name
```
Then open a PR into `dev`. Merge to `main` only once a feature is tested and stable.

**Before pushing, always double-check `.env` isn't staged:**
```bash
git status
```

---

Internal team repository. Do not share externally.
