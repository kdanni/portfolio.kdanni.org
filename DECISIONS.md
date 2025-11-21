# Architecture & Tech Stack Decisions

This file tracks the key architectural decisions and technology selections for the AssetManager project.

## Status
- **Languages:** Python 3.12+ / Node.js (LTS)
- **Web Frameworks:** FastAPI / Express.js
- **Database:** PostgreSQL
- **Authentication:** [Pending Selection]

## Decisions Log

### 2025-11-21 - Tech Stack Selection (Node.js/Express Addition)
**Context:**
The user requested to "also add" a Node.js + Express API layer solution. This implies the system may support multiple implementations (e.g., for benchmarking, migration, or polyglot support) or offer an alternative backend path while sharing the same database.

**Decision:**
1.  **Secondary Language:** Node.js (LTS Version)
    *   Chosen for its ubiquity, non-blocking I/O model, and vast ecosystem.
2.  **Secondary Web Framework:** Express.js
    *   Chosen as the standard, minimalist web framework for Node.js. It allows for flexible architecture implementation (Clean Architecture) without imposing a strict structure.
3.  **Shared Architecture:**
    *   The Node/Express implementation will adhere to the same **"Smart Database Schema"** philosophy.
    *   It will connect to the *same* PostgreSQL schema.
    *   It will implement a matching Repository Pattern to interface with the DB.
    *   Data validation will use libraries like `Joi` or `Zod` to mirror the strictness of Pydantic in the Python version.

**Consequences:**
*   The project structure may need to be reorganized to separate `src/python` and `src/node` if both are maintained simultaneously.
*   We must ensure the Database Schema (SQL) remains the single source of truth, agnostic to the API layer language.
*   Tests must be adaptable or replicated for the Node.js implementation.

### 2025-11-21 - Tech Stack Selection (Python/FastAPI/PostgreSQL)
**Context:**
We needed to select a technology stack that satisfies the requirement for a "Lightweight" but "Robust" system (ACID compliance, <100ms latency). The system is a backend-only financial asset manager. The user also specified a preference for "Standalone DB logic" where the database enforces validity independently of the application layer.

**Decision:**
1.  **Language:** Python 3.12+
    *   Chosen for its extensive ecosystem in financial data, development speed, and strong typing capabilities (via Type Hints).
2.  **Web Framework:** FastAPI
    *   Chosen for high performance (ASGI), built-in data validation (Pydantic), and automatic OpenAPI documentation.
3.  **Database:** PostgreSQL
    *   Chosen as the primary RDBMS. It offers superior support for strict data integrity (CHECK constraints, JSONB, robust transaction handling) compared to alternatives like MySQL, aligning with the "Robustness" requirement.
4.  **Architecture Pattern:** Smart Database Schema + Repository Pattern
    *   We will use PostgreSQL features (Constraints, Foreign Keys) to act as the primary enforcer of data correctness (Standalone DB Logic).
    *   The Python layer will use the Repository pattern to interface with the DB, translating DB constraints into API responses, ensuring Clean Architecture while leveraging the DB's power.

**Consequences:**
*   We must write SQL or use a migration tool (like Alembic) that supports defining advanced constraints (CHECK, etc.).
*   Application logic for validation will be minimal, relying on Pydantic for shape validation and the DB for state/business rule validation where possible.
*   Deployment will require a PostgreSQL instance.
