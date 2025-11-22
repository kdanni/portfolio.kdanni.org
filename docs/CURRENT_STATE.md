# Current State of Repository

**Date:** 2025-02-21

## 1. Overview
The **AssetManager** repository is initialized with a dual-backend structure (Python and Node.js) sharing a single PostgreSQL database. The project follows a **Clean Architecture** pattern and prioritizes data integrity via a "Smart Database Schema".

## 2. Directory Structure
The repository is organized into source code (`src`), documentation (`docs`), and tests (`tests`).

```
.
├── docs/                   # Documentation (Requirements, Testing, Architecture)
├── src/
│   ├── python/             # Primary Backend (FastAPI)
│   │   ├── api/            # Routers, Schemas, Dependencies
│   │   ├── core/           # Domain Entities, Repository Interfaces
│   │   ├── infrastructure/ # DB Access (Models, Repository Implementations)
│   │   └── alembic/        # DB Migrations
│   └── node/               # Secondary Backend (Express)
│       └── ...             # Setup with package.json
├── tests/                  # Test Suites
└── docker-compose.yml      # Infrastructure (PostgreSQL)
```

## 3. Technology Stack Status

### 3.1 Infrastructure
*   **Docker Compose:** Configured to run PostgreSQL 15 (Alpine) on port 5432.
*   **Database:** PostgreSQL is the source of truth.

### 3.2 Python Backend (Primary)
*   **Status:** Core, Infrastructure, and API Layers Implemented for base entities.
*   **Framework:** FastAPI (installed).
*   **ORM:** SQLAlchemy 2.0+ (installed).
*   **Migrations:** Alembic (configured).
*   **Dependencies:** Managed via `poetry` (`pyproject.toml` present).
*   **Implemented Code:**
    *   **Domain:** `Asset`, `Exchange`, `Listing` entities defined.
    *   **Infrastructure:**
        *   Models: `AssetModel`, `ExchangeModel`, `ListingModel`.
        *   Repositories: `SqlAlchemyAssetRepository`, `SqlAlchemyExchangeRepository`, `SqlAlchemyListingRepository`.
    *   **API:**
        *   Routers: `/assets`, `/exchanges`, `/listings` implemented with CRUD operations.
        *   Schemas: Pydantic models for request/response validation.

### 3.3 Node.js Backend (Secondary)
*   **Status:** Initial Setup.
*   **Framework:** Express.js (installed).
*   **DB Driver:** `pg` (installed).
*   **Dependencies:** Managed via `npm` (`package.json` present).
*   **Implemented Code:** None (scaffold only).

## 4. Database Schema Snapshot
Currently, the schema defines three core entities: **Assets**, **Exchanges**, and **Listings**.

| Table | Column | Type | Constraints |
| :--- | :--- | :--- | :--- |
| **assets** | `id` | Integer | PK, Auto-inc |
| | `name` | String(255) | Length > 0 |
| | `asset_class` | Enum | Not Null |
| | `isin` | String(12) | Unique, Nullable |
| | `is_active` | Boolean | Default True |
| **exchanges** | `id` | Integer | PK, Auto-inc |
| | `name` | String(255) | Length > 0 |
| | `mic_code` | String(20) | Unique, Not Null |
| | `currency` | String(10) | Not Null |
| **listings** | `id` | Integer | PK, Auto-inc |
| | `asset_id` | Integer | FK to assets.id |
| | `exchange_id` | Integer | FK to exchanges.id |
| | `ticker` | String(20) | Not Null |
| | `currency` | String(10) | Not Null |

## 5. Next Steps
*   Design and implement `Portfolios` schema.
*   Mirror functionality in Node.js backend.
