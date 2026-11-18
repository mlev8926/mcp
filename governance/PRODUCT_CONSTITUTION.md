# NEXUS SaaS — Product Constitution

Status: APPROVED PRODUCT DIRECTION for the decisions explicitly stated by the project owner. This document is not a substitute for approval of unresolved technical choices.

## Approved product direction

- Product model: both multi-tenant SaaS and self-hosted/on-premise distribution.
- Module engine: dynamic, with explicit module lifecycle and contracts.
- Deployment model: hybrid.
- Quality objective: enterprise-level engineering, strong resiliency, security, tenant isolation, and a stable core. "Zero crash" is a quality aspiration, not a mathematically guaranteeable claim.

## Product implications

1. The platform must support a hosted SaaS operating model and a separately deployable self-hosted/on-premise model.
2. The platform core must remain independent from optional business modules.
3. Modules must be discoverable and governed through versioned manifests, dependency declarations, permissions, compatibility rules, and lifecycle contracts.
4. The system must provide controlled install, enable, disable, upgrade, rollback, and uninstall workflows.
5. Tenant boundaries must be enforced consistently across APIs, background jobs, data access, events, caches, files, and observability.
6. Hybrid deployment must be designed as a product capability, not a last-minute packaging exercise.
7. AI-generated changes must be traceable, testable, reviewed, and consistent with approved decisions.

## Explicit non-goals for the initial foundation

- Do not assume the Nexus SaaS application repository already exists.
- Do not generate a production application before the owner approves the architecture decision register and initial build phase.
- Do not silently choose vendors, cloud providers, payment gateways, regions, or compliance certifications.
