# Technical Requirements & Constraints

**Document Version:** 1.0
**Status:** Draft
**Date:** [Current Date]

## 1. Overview
This document defines the technical requirements, constraints, and performance targets for the **AssetManager** backend system. The system is envisioned as a lightweight but robust source of truth for financial asset definitions and portfolio structures.

## 2. System Characteristics
*   **Lightweight:** The system should have minimal operational overhead. It should be easy to spin up (e.g., via Docker Compose) and resource-efficient.
*   **Robust:** As a system dealing with financial data concepts, correctness and data integrity are prioritized over raw throughput.
*   **Modular:** The architecture must strictly separate concerns (API vs. Core vs. Infrastructure) to allow for future technology swaps or scaling.

## 3. Non-Functional Requirements

### 3.1 Data Persistence & Integrity
*   **Consistency Model:** Strict consistency is required. Financial data (even reference data) must not be subject to eventual consistency anomalies during updates.
    *   *Requirement:* **ACID compliance** is mandatory.
    *   *Implication:* A Relational Database (RDBMS) is the primary candidate (PostgreSQL or SQLite for dev).
*   **Data Durability:** Committed transactions must survive system crashes.

### 3.2 Latency & Performance
*   **Read Latency:** API response time for standard read operations (e.g., "Get Portfolio", "List Assets") should be **< 100ms** (excluding network RTT) for the 95th percentile (p95).
*   **Write Latency:** API response time for write operations should be **< 200ms**.
*   **Throughput:** Initial target: Support single-user or small-team usage.
    *   *Constraint:* The system does not currently need to support "Internet Scale" or High Frequency Trading (HFT) loads.

### 3.3 Scalability
*   **Vertical Scaling:** The system should run efficiently on a single low-cost VPS (e.g., 1 vCPU, 512MB - 1GB RAM).
*   **Horizontal Scaling:** While not required for MVP, the application tier should be stateless to allow for future load balancing if needed.

### 3.4 Security
*   **Authentication:** All API endpoints (except health checks/public docs) must be secured.
    *   *Requirement:* Token-based authentication (e.g., Bearer Token).
*   **Authorization:** The system must support basic role/ownership checks (e.g., User A cannot modify User B's portfolio).
*   **Input Validation:** Strict validation of all incoming data types (e.g., Ticker symbols, numeric values).

### 3.5 Observability
*   **Logging:** Structured logging (JSON) for all API requests and background tasks.
*   **Health Checks:** Dedicated `/health` endpoint for container orchestration.

## 4. Functional Requirements (High-Level)

### 4.1 Domain: Asset Catalog
*   System must support creating, reading, updating, and deleting (CRUD) Asset definitions.
*   **Assets** must have unique identifiers (e.g., ISIN, Internal ID) and standard metadata (Ticker, Name, Asset Class).
*   Support filtering/searching assets (e.g., "Find all Stocks").

### 4.2 Domain: Portfolio
*   Users can create multiple **Portfolios**.
*   Portfolios serve as containers for Assets (Implementation of actual Holdings is Phase 4, but the container structure is Phase 1/2).

### 4.3 API Surface
*   The API must be versioned (e.g., `/api/v1/...`).
*   Standard HTTP Status codes must be used correctly (200, 201, 400, 404, 500).
*   Documentation (OpenAPI/Swagger) should be auto-generated from code where possible.

## 5. Constraints
*   **No Frontend:** The project is strictly a backend API.
*   **Containerization:** The entire stack must be runnable via `docker compose up`.
