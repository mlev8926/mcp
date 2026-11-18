# NEXUS SaaS — Architecture Constitution

> Status: STARTER BASELINE. Treat each decision below as proposed until explicitly approved by the project owner.

## Product and deployment
- Product target: SaaS and self-hosted/on-premise.
- Deployment model: hybrid.
- Module engine: dynamic, contract-driven lifecycle.

## Suggested technical baseline
- Backend: Python 3.11+ with FastAPI.
- Frontend: Next.js + TypeScript.
- Architecture: modular monolith with Clean/Hexagonal boundaries.
- Primary transactional database: PostgreSQL.
- Multi-tenancy: tenant-scoped data access with tenant_id and database-enforced Row-Level Security where applicable.
- Platform separation: Control Plane and Data Plane.
- Modules communicate through explicit contracts and versioned domain events.

## Non-negotiable governance
1. Do not silently change an approved architecture decision.
2. Distinguish approved decisions from observations and proposals.
3. Module installation, activation, upgrade, and rollback must not destabilize the core.
4. Enforce tenant isolation at every data boundary.
5. Migrations must be versioned, reviewable, and recoverable.
6. If a decision is not documented, mark it UNKNOWN and ask before assuming.
