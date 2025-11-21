# 🏦 AssetManager (Backend API)

**Current Status:** `Phase 0: Initialization & Design`
**Scope:** Backend Database & API Layer (No Frontend)

---

## 🤖 Agent Context & Directives
**ATTENTION AI AGENTS:** Read this section first. This project is a collaboration between a single Human Developer and AI Agents.

1.  **Role:** You are a Senior Backend Architect and DevOps Engineer.
2.  **Scope Constraint:** This project is **strictly** a Database and API layer. Do not generate frontend code (HTML/CSS/React) unless explicitly requested for documentation/visualization purposes.
3.  **Tech Stack Selection:** Currently in the selection phase. Do not assume a stack (e.g., Django vs. Node) until `DECISIONS.md` is updated.
4.  **Code Style:** Modular, strongly typed (where applicable), and heavily commented for future context retrieval.
5.  **Documentation:** Every major architectural decision must be logged in `docs/adr/`.

---

## 🎯 Project Vision
A lightweight, robust backend system to manage financial asset data. The system serves as the source of truth for asset definitions and portfolio structures.

### Core Domains
1.  **Asset Catalog (Reference Data):** The universe of available assets (Stocks, Crypto, ETFs, etc.) with metadata (Ticker, ISIN, Name, Asset Class).
2.  **Asset Portfolio (Container):** Logical groupings of assets owned by a user (e.g., "Retirement Fund," "Speculative Crypto").
3.  **Holdings (Vision/Future):** The intersection of *Portfolio* and *Catalog*, tracking quantity, average buy price, and current value.

---

## 🗺️ Development Roadmap

We are following an incremental development path.

### Phase 1: Initialization & Design (📍 WE ARE HERE)
- [x] Create Repository & README
- [x] **Task 1.1:** Define Technical Requirements (Latency, Persistence, Scalability). (See [docs/TECHNICAL_REQUIREMENTS.md](docs/TECHNICAL_REQUIREMENTS.md))
- [ ] **Task 1.2:** Select Technology Stack (Language, Framework, DB).
- [ ] **Task 1.3:** Design High-Level IT Architecture.
- [ ] **Task 1.4:** Design Domain Schema (ERD) for Catalog and Portfolio.

### Phase 2: Scaffold & Environment
- [ ] Set up Docker/Containerization.
- [ ] Initialize API Framework (Hello World).
- [ ] Set up Database Migration tool.

### Phase 3: Implementation - Asset Catalog
- [ ] Create CRUD endpoints for Assets.
- [ ] Implement Search/Filter logic.
- [ ] Seed database with sample market data.

### Phase 4: Implementation - Portfolios
- [ ] Create CRUD endpoints for Portfolios.
- [ ] Link Portfolios to Assets (Holdings logic).

---

## 🏗 Architecture & Stack

**Note:** This section is currently *Under Construction*. The goal of the first sprint is to fill this in.

### Target Architecture
We aim for a clean separation of concerns, likely following a Layered or Hexagonal architecture.



[Image of web application architecture diagram]


### Candidate Technologies
- **Language:** Python (FastAPI/Django) OR Go (Chi/Gin) OR TypeScript (NestJS).
- **Database:** PostgreSQL (Relational data is crucial for financial consistency) OR SQL-lite (for lightweight start).
- **Containerization:** Docker & Docker Compose.

---

## 📂 Project Structure (Standard)

Agents must adhere to this directory structure to maintain context.

```text
/
├── docs/
│   ├── adr/                 # Architecture Decision Records
│   └── schema/              # ER diagrams and SQL drafts
├── src/
│   ├── api/                 # Controllers/Routes
│   ├── core/                # Business Logic & Domain Models
│   └── infrastructure/      # DB connections, External APIs
├── tests/
├── scripts/                 # Utility scripts for agents
├── .env.example
├── DECISIONS.md             # Log of agreed tech stack choices
└── README.md
```


## Setup Instructions
(To be populated after Tech Stack selection)

1. Clone repository.
2. Copy .env.example to .env.
3. Run [init command].

---

## 🤝 Contribution Protocol for Agents
When tasked with a code change:

1. Check DECISIONS.md first to ensure alignment with the selected stack.
2. Propose the file structure before writing full code.
3. Update the Current Status in this README if a phase is completed.
