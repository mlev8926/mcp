# Validation plan and evidence

## Automated CI

GitHub Actions runs on pushes to `main` and `feature/**`, pull requests, and manual dispatch. It tests Python 3.11, 3.12, and 3.13; installs package/development dependencies; compiles source and tests; and runs pytest.

## Coverage

- MCP tool discovery and invocation for all 11 tools.
- Blueprint, decision register, architecture context, and workspace status.
- MCP resources for status, architecture, build blueprint, and decisions.
- Governance-first mode when no SaaS application workspace exists.
- File safety: path traversal and secret-file rejection.
- Indexer safety: secrets, internal snapshot files, and external symlinks.
- Real STDIO subprocess transport.

## Codex integration

Configure `NEXUS_GOVERNANCE_ROOT` to this MCP repository. Leave `NEXUS_WORKSPACE_ROOT` unset while the SaaS application repository has not yet been created. After the owner creates/selects the application repository, configure both roots separately.

Use `integrations/codex-config.toml.example` and `integrations/AGENTS.md`. Restart Codex and inspect `/mcp`; verify that all 11 tools are listed. Then ask the agent to bootstrap and report the workspace state.

## What CI does not prove

CI does not prove production reliability, complete secret detection, semantic correctness, security certification, enterprise readiness, or zero-crash behavior. Real-host integration, threat modeling, deployment tests, and operational validation remain necessary.
