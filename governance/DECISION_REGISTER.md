# NEXUS SaaS — Architecture Decision Register

This register is the authority for decision status. The AI must not promote PROPOSED or UNKNOWN items to APPROVED without explicit owner approval.

## APPROVED

| ID | Decision | Approved direction |
|---|---|---|
| NEXUS-PROD-001 | Product model | Both SaaS and self-hosted/on-premise |
| NEXUS-PLAT-001 | Module engine | Dynamic, contract-driven |
| NEXUS-DEP-001 | Deployment model | Hybrid |
| NEXUS-GOV-001 | AI governance | MCP is the architecture and project-governance source for AI-assisted development |

## PROPOSED — requires owner approval

| ID | Decision area | Current candidate only |
|---|---|---|
| NEXUS-TECH-001 | Backend framework | Python + FastAPI |
| NEXUS-TECH-002 | Frontend | Next.js + TypeScript |
| NEXUS-ARCH-001 | Application architecture | Modular monolith with Clean/Hexagonal boundaries |
| NEXUS-DATA-001 | Primary database | PostgreSQL |
| NEXUS-TEN-001 | Tenant isolation strategy | Tenant-scoped data access, with database-enforced RLS where applicable |
| NEXUS-PLAT-002 | Platform topology | Control Plane / Data Plane separation |
| NEXUS-EVT-001 | Internal integration | Versioned domain events and explicit module contracts |

These are candidate options for evaluation, not final technical requirements.

## UNKNOWN — must be resolved before implementation depends on them

- Initial target industries and first business workflows.
- SaaS tenant isolation tiering (shared schema, schema-per-tenant, database-per-tenant, or supported combination).
- Identity provider, authentication protocols, SSO, MFA, and enterprise identity requirements.
- Cloud provider, supported deployment targets, Kubernetes/container requirements, and offline/on-premise constraints.
- Queue/event broker, cache, search engine, object storage, and observability stack.
- Billing provider, tax/invoicing requirements, subscription model, and payment integrations.
- Data residency, backup retention, RPO/RTO, disaster recovery, and compliance scope.
- Module packaging format, signing/trust model, sandboxing, permissions, and compatibility policy.
- API versioning policy and external developer ecosystem.
- Localization, currency, timezone, and regional requirements.
- Initial MVP scope and release acceptance criteria.

## Approval protocol

1. AI creates a proposal with `nexus_propose_adr`.
2. Proposal must state context, options, trade-offs, security impact, migration impact, and rollback plan.
3. Project owner explicitly approves or rejects.
4. Only after approval may the register and constitution be updated.
5. Every implementation change cites the relevant decision IDs.
