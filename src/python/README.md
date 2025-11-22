# Python Backend

This directory contains the FastAPI service for AssetManager. Use it as the working directory for development commands so the `api`, `core`, and `infrastructure` packages are on the Python path.

## Running the API Server

```bash
# Start the Postgres container from the repository root if you haven't already
# docker compose up -d

cd src/python
poetry install
poetry run alembic upgrade head
poetry run fastapi dev api/main.py  # Hot reload during development
# or
poetry run uvicorn api.main:app --reload
```

The server exposes:
- `GET /health` for a simple health check.
- `POST /assets/` to create an asset.
- `GET /assets/{asset_id}` to fetch a single asset.
- `GET /assets/` to list all assets.

All database connection settings are read from the `POSTGRES_*` environment variables (see `infrastructure/database/base.py` for defaults). When running commands from the repository root, set `PYTHONPATH=src/python` to make the modules importable.

## Running Tests

```bash
cd src/python
poetry run pytest ../../tests/python
```

The API tests run against an in-memory SQLite database. Repository integration tests rely on the configured Postgres instance.
