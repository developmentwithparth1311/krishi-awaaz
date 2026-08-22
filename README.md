# Krishi Awaaz

**A voice-first AI agent system for fair agricultural price negotiation.**

Farmers call a single phone number, speak naturally in their own language, and an autonomous multi-agent pipeline finds the best buyers, negotiates on their behalf, and reports back — no app, no typing, no literacy barrier.

<p align="left">
  <img alt="Status" src="https://img.shields.io/badge/status-in%20development-yellow">
  <img alt="Language" src="https://img.shields.io/badge/language-Python-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen">
  <img alt="Made for" src="https://img.shields.io/badge/made%20for-Agentic%20AI%20track-orange">
</p>

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Team & Ownership](#team--ownership)
- [Git Workflow](#git-workflow)
- [Roadmap](#roadmap)

---

## Overview

Most Indian farmers sell to the first middleman who shows up, not because that's the best price, but because they have no real-time visibility into mandi prices and no easy way to contact multiple buyers. Existing digital solutions (apps, web portals) largely assume literacy and smartphone comfort that a huge portion of this population doesn't have.

**Krishi Awaaz removes that barrier entirely.** The phone call *is* the interface. A farmer dials in, talks naturally, and a pipeline of AI agents does the rest — price research, buyer ranking, live negotiation calls, and a plain-spoken result.

## How It Works

```
Farmer calls in
      │
      ▼
Caller ID check ──► Unknown number ──► Voice-based onboarding
      │
   Known number
      │
      ▼
Intake Agent          (understands crop, quantity, location, urgency)
      │
      ▼
Decision Agent         (ranks buyers using live price + transport + urgency data)
      │
      ▼
Negotiation Agent      (calls buyers, negotiates within a floor price)
      │
      ▼
Report Agent           (tells the farmer the result, in their language)
```

Full architecture details live in [`docs/architecture.md`](docs/architecture.md).

## Tech Stack

| Layer | Tool |
|---|---|
| Telephony (inbound/outbound calls) | Twilio / Exotel |
| Speech-to-Text | Sarvam AI — Saaras |
| Text-to-Speech | Sarvam AI — Bulbul |
| Conversational reasoning | Sarvam-30B |
| Decision / negotiation reasoning | Sarvam-105B (or Claude/GPT with tool use) |
| Market price data | Agmarknet API |
| Database | PostgreSQL via Supabase |
| Orchestration | Python state machine |

## Project Structure

```
krishi-awaaz/
├── telephony/          # Call handling, STT/TTS pipeline
├── agents/              # Intake, Decision, Negotiation, Report agent logic
│   └── prompts/         # Prompt templates, kept separate from code
├── orchestration/        # Pipeline coordination, auth, error handling
├── data/                # Agmarknet, weather, transport cost, price ranking
├── db/                   # Supabase client, schema, queries
├── dashboard/            # Live call-status dashboard for demos
├── tests/                # Unit + integration tests
├── scripts/              # One-off setup/utility scripts
└── docs/                 # Architecture, API reference, demo script, setup guide
```

| Folder | Owns |
|---|---|
| `telephony/` | Call flow, audio pipeline, latency |
| `agents/` | All LLM prompts and reasoning logic |
| `orchestration/` | Wiring agents together, auth, failure handling |
| `data/` | External API integrations and ranking math |
| `db/` | Schema and all database reads/writes |
| `dashboard/` | Visual demo of the pipeline running live |
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
Run `db/schema.sql` against your Supabase project to create the required tables.

**5. Seed test data (optional, for local development)**
```bash
python scripts/seed_test_data.py
```

**6. Run a local test**
```bash
python scripts/run_local_demo.py
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
SARVAM_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
AGMARKNET_API_KEY=
WEATHER_API_KEY=
LLM_API_KEY=
```

Ask in the team group chat if you need any of these keys — do not generate your own unless told to.

## Team & Ownership

| Person | Focus Area |
|---|---|
| Person A | Telephony & voice pipeline (`telephony/`) |
| Person B | Agent logic & prompts (`agents/`) |
| Person C | Backend, database & orchestration (`orchestration/`, `db/`) |
| Person D | Data integration, dashboard, testing (`data/`, `dashboard/`, `tests/`) |

Replace this table with actual names once roles are locked in.

## Git Workflow

```
main            → always stable, demo-ready
dev             → integration branch, merge feature branches here first
feature/*       → e.g. feature/intake-agent, feature/outbound-calling
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

## Roadmap

- [ ] Week 1 — Environment setup, API access, DB schema
- [ ] Week 2 — Core voice loop (inbound call → STT → response → TTS)
- [ ] Week 3 — Intake agent + onboarding, fully working
- [ ] Week 4 — Decision agent (price ranking logic)
- [ ] Week 5 — Negotiation agent (outbound calling)
- [ ] Week 6 — Report agent + full pipeline integration
- [ ] Week 7 — Extensions, testing, demo prep

Full detailed week-by-week plan lives in [`docs/setup_guide.md`](docs/setup_guide.md).

---

Built for the Agentic AI track. Contributions from team members welcome via pull requests into `dev`.
