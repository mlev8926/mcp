# NEXUS MCP — Architecture Governance Engine

NEXUS MCP is the blueprint, architecture-governance, and AI coding control layer for building Nexus SaaS from zero. The SaaS application itself is **not assumed to exist**.

## Two separate roots

- **Governance root:** this repository (`mlev8926/mcp`). It stores the product constitution, architecture constitution, decision register, build blueprint, quality gates, module contracts, and AI rules.
- **Development workspace:** the future Nexus SaaS application repository. It is optional and can remain unset until the owner authorizes application creation.

Do not point the governance root at a future app directory. Do not treat a proposed framework as approved architecture.

## Approved product direction

- Product model: both SaaS and self-hosted/on-premise.
- Module engine: dynamic and contract-driven.
- Deployment model: hybrid.
- Quality goal: enterprise-grade resilience, security, tenant isolation, and stable core. "Zero crash" is an aspiration, not a guarantee.

The backend, frontend, database, tenant topology, identity, cloud, queue, and other technical decisions remain PROPOSED or UNKNOWN unless explicitly approved in `governance/DECISION_REGISTER.md`.

## Governance documents

- `governance/PRODUCT_CONSTITUTION.md` — approved product direction.
- `governance/ARCHITECTURE_CONSTITUTION.md` — architecture principles and boundaries.
- `governance/DECISION_REGISTER.md` — APPROVED, PROPOSED, and UNKNOWN decisions.
- `governance/BUILD_BLUEPRINT.md` — staged build plan from zero to enterprise release.
- `governance/ENTERPRISE_QUALITY_GATES.md` — evidence-based engineering and release gates.
- `governance/MODULE_CONTRACT_TEMPLATE.md` — module contract starter.
- `governance/AI_CODING_RULES.md` — mandatory AI workflow.

## AutoLearn / project-context synchronization

NEXUS MCP maintains a project file index and exposes tools/resources to compatible AI hosts. It does not retrain model weights or silently inject every changed file into a model. The host must call bootstrap, read relevant documents/files, and sync after changes. The optional watcher refreshes the local snapshot only.

## Install and validate

Requirements: Python 3.11+ and uv.

```bash
uv sync --all-groups
uv run pytest -q
```

## Configure Codex before the application exists

Set only the governance root. Leave `NEXUS_WORKSPACE_ROOT` unset until the owner creates or selects the Nexus SaaS application workspace.

```bash
codex mcp add nexus \
  --env NEXUS_GOVERNANCE_ROOT=/absolute/path/to/mcp \
  -- uv run --project /absolute/path/to/mcp python -m nexus_mcp.server
codex mcp list
```

Or merge `integrations/codex-config.toml.example` into `~/.codex/config.toml`, replacing the path.

After connecting, restart Codex and use `/mcp` to confirm the server. At session start, the agent must call:

1. `nexus_bootstrap_context`
2. `nexus_get_architecture_context`
3. `nexus_get_build_blueprint`
4. `nexus_get_decision_register`
5. `nexus_get_workspace_status`

Copy `integrations/AGENTS.md` into the root of a future Nexus SaaS workspace when that workspace is created.

## Configure the future application workspace

Once the owner creates/selects the application repository, add the following environment variable to the MCP server configuration:

```toml
[mcp_servers.nexus.env]
NEXUS_GOVERNANCE_ROOT = "/absolute/path/to/mcp"
NEXUS_WORKSPACE_ROOT = "/absolute/path/to/nexus-saas"
```

Both directories must be separate and exist. Until then, MCP operates in blueprint/governance mode and indexes its own governance repository.

## MCP tools

- `nexus_bootstrap_context` — mandatory session start and context refresh.
- `nexus_sync_project_context` — refresh index and report file deltas.
- `nexus_project_status` — report governance readiness and workspace state.
- `nexus_get_build_blueprint` — staged application build plan.
- `nexus_get_decision_register` — approved/proposed/unknown architecture decisions.
- `nexus_get_workspace_status` — confirm whether an application workspace is configured.
- `nexus_search_project` — search active workspace, or governance repository before workspace creation.
- `nexus_read_project_file` — read a safe text file within the active root.
- `nexus_get_architecture_context` — read product/architecture/AI governance.
- `nexus_validate_change` — deterministic guardrails, not a formal security audit.
- `nexus_propose_adr` — create an unapproved proposal; does not change approved decisions.

Resources:
- `nexus://project/status`
- `nexus://architecture/context`
- `nexus://blueprint/build`
- `nexus://governance/decisions`

## Security and limitations

- Reads are constrained to the active root; common secrets, private-key files, and symlinks are excluded/rejected.
- ADR proposals are not approved automatically.
- Deterministic validation is not semantic proof, a complete secret scanner, security audit, or zero-crash guarantee.
- A successful CI run validates the tested code paths only; real-host integration and production readiness require separate evidence.
