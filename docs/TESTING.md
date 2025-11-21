# Testing Strategy

This document outlines the testing strategy for the AssetManager project.

## Overview

We follow the "Testing Pyramid" approach:
1.  **Unit Tests:** Fast, isolated tests for domain logic.
2.  **Integration Tests:** Tests that verify interaction with the database and other infrastructure components.
3.  **E2E Tests:** Full system tests (future scope).

## Python Testing

We use `pytest` for Python testing.

### Directory Structure

Tests are located in `tests/python`.

### Running Tests

To run all tests:
```bash
cd src/python
poetry run pytest ../../tests/python
```

### Integration Tests (Database)

Integration tests require a running database.
1.  Ensure Docker Compose is up: `docker compose up -d`
2.  The tests will connect to the local PostgreSQL instance. *Note: In a real CI/CD pipeline, we would spin up a dedicated test container.*

## Node.js Testing

(To be implemented)
We will use `jest` for Node.js testing.
