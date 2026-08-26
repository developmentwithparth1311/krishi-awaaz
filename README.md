# Krishi Awaaz simulation

This repository contains the text-first simulation layer for Krishi Awaaz. It deliberately
does not contain voice or real telephony yet. The purpose of this stage is to make the farmer
intake, market comparison, middleman negotiation, ranking, and reporting behavior visible and
repeatable before speech recognition makes the inputs less predictable.

All names, phone aliases, market prices, and commercial terms in `data/scenarios.json` are
fictional test data. They must not be treated as current market information or real offers.

## Current architecture

```text
Scripted multilingual farmer conversation
    -> Intake node (typed FarmerRequest)
    -> Decision node (synthetic market net-return comparison)
    -> Buyer-selection node (crop and quantity constraints)
    -> Parallel deterministic negotiation nodes
    -> Offer ranker (risk-adjusted net return)
    -> Non-binding farmer report
```

Plain Python defines the node order and shared state, while `asyncio.gather` runs independent
middleman negotiations concurrently. All domain models, price rules, negotiation rules, and
PostgreSQL persistence remain ordinary Python modules.

The catalog currently covers four farmers speaking Marathi, Punjabi, Tamil, and Telugu, with
three middlemen per farmer. Every non-English conversation line includes an English translation
for review.

## Project structure

```text
krishi-awaaz/
├── telephony/           # Reserved for call handling and audio
├── agents/              # Domain models, negotiation logic, language templates
│   └── prompts/         # Reserved for future model prompts
├── orchestration/       # Plain-Python workflow, configuration, CLI
├── data/                # Scenario loader and synthetic multilingual fixtures
├── db/                  # PostgreSQL schema and persistence
├── dashboard/           # Reserved for the future internal dashboard
├── tests/               # Unit and workflow tests
├── scripts/             # Reserved for setup and utility scripts
├── docs/                # Reserved for internal documentation
└── krishi_awaaz/        # Compatibility launcher for `python -m krishi_awaaz`
```

Only the components already implemented contain application code. The telephony, dashboard,
prompts, scripts, and docs folders are placeholders for later project stages.

## Set up Python

Python 3.11 or newer is required.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

List and inspect the fixtures:

```powershell
krishi-sim list
krishi-sim show nashik-onion-001
```

Run a complete simulation without requiring PostgreSQL:

```powershell
krishi-sim run nashik-onion-001 --no-db
```

Use `--json` when you want the typed output rather than the review-oriented transcript.

## PostgreSQL

The application only accepts a PostgreSQL SQLAlchemy URL for persistence. It does not silently
fall back to SQLite.

If Docker is available:

```powershell
docker compose up -d postgres
Copy-Item .env.example .env
$env:DATABASE_URL = "postgresql+psycopg://krishi:krishi@localhost:5432/krishi_awaaz"
krishi-sim db-init
krishi-sim run nashik-onion-001
```

The schema stores:

- simulated farmer profiles and locations;
- produce listings and minimum-price constraints;
- synthetic market snapshots and logistics estimates;
- simulated middleman profiles and hidden test constraints;
- simulation runs and workflow events;
- every original-language message and its English translation;
- provisional offers, costs, rankings, and risk-adjusted totals.

`db-init` uses SQLAlchemy metadata to create the initial schema and upsert the fixture
participants. Before a real deployment, schema evolution should be moved to Alembic migrations.

## Important simulation boundaries

- The intake transcript is scripted and validated into a `FarmerRequest`; it does not yet test
  speech recognition or free-form information extraction.
- A middleman's maximum price is hidden simulator state. It is available in `krishi-sim show`
  for reviewers, but the negotiation algorithm never receives it as market evidence.
- Quotes are explicitly provisional. The workflow never creates a binding sale.
- Market observations and transport costs are synthetic fixtures.
- Ranking prefers risk-adjusted net return, not the largest headline price.

These boundaries are intentional. A later voice adapter can supply transcripts to the same
typed workflow without changing the negotiation and ranking contracts.
