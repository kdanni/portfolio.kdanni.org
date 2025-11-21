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
│   │   ├── api/            # Controllers (Empty)
│   │   ├── core/           # Business Logic (Empty)
│   │   ├── infrastructure/ # DB Access
│   │   │   ├── database/   # SQLAlchemy Models (AssetModel implemented)
│   │   │   └── repositories/ # Data Access Objects (Empty)
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
*   **Status:** Initial Setup & Partial Infrastructure Layer.
*   **Framework:** FastAPI (installed).
*   **ORM:** SQLAlchemy 2.0+ (installed).
*   **Migrations:** Alembic (configured).
*   **Dependencies:** Managed via `poetry` (`pyproject.toml` present).
*   **Implemented Code:**
    *   `AssetModel` (`src/python/infrastructure/database/models.py`): Defines the `assets` table with columns (`id`, `ticker`, `name`, `asset_class`, `is_active`) and CHECK constraints.

### 3.3 Node.js Backend (Secondary)
*   **Status:** Initial Setup.
*   **Framework:** Express.js (installed).
*   **DB Driver:** `pg` (installed).
*   **Dependencies:** Managed via `npm` (`package.json` present).
*   **Implemented Code:** None (scaffold only).

## 4. Database Schema Snapshot
Currently, the schema defines a single entity: **Assets**.

| Table  | Column | Type | Constraints |
| :--- | :--- | :--- | :--- |
| **assets** | `id` | Integer | PK, Auto-inc |
| | `ticker` | String(20) | Unique, Length > 0 |
| | `name` | String(255) | Length > 0 |
| | `asset_class` | String(50) | Not Null |
| | `is_active` | Boolean | Default True |
| | `created_at` | DateTime | Server Default Now |
| | `updated_at` | DateTime | Server Default Now |

## 5. Next Steps
*   Implement Python Core layer (Use Cases).
*   Implement Python API layer (Endpoints).
*   Design and implement `Portfolios` schema.
*   Mirror functionality in Node.js backend.
