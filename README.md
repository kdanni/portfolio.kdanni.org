# AssetManager

AssetManager is a lightweight, robust backend system for managing financial asset definitions and portfolio structures. It is designed with a "Smart Database Schema" philosophy, where the database enforces data integrity.

## Tech Stack

*   **Primary Backend:** Python 3.12+ with FastAPI
*   **Secondary Backend:** Node.js LTS with Express.js
*   **Database:** PostgreSQL
*   **Migration Tool:** Alembic (Python)

## Getting Started

### Prerequisites

*   Docker & Docker Compose
*   Python 3.12+ & Poetry
*   Node.js LTS & npm

### Environment Setup

1.  **Start the Database**:
    ```bash
    docker compose up -d
    ```
    This spins up a PostgreSQL instance on port 5432.

2.  **Python Setup**:
    ```bash
    cd src/python
    poetry install
    # Apply migrations
    poetry run alembic upgrade head
    ```

3.  **Node.js Setup** (Optional/Future):
    ```bash
    cd src/node
    npm install
    ```

## Project Structure

*   `src/python`: Python backend implementation (FastAPI, SQLAlchemy, Alembic).
    *   `api`: API endpoints (Controllers).
    *   `core`: Domain logic and interfaces.
    *   `infrastructure`: Database models, repositories, and external services.
*   `src/node`: Node.js backend implementation (Express).
*   `docs`: Documentation and Architecture Decision Records (ADRs).

## Testing

See `docs/TESTING.md` for detailed testing instructions.
