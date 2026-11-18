# Validation plan and evidence

## Automated checks

The GitHub Actions workflow `.github/workflows/ci.yml` runs on pushes to `main` and `feature/**`, pull requests, and manual dispatch.

It tests Python 3.11, 3.12, and 3.13; installs the package and development dependencies; compiles source and tests; then runs pytest.

## Test coverage

- MCP protocol tool discovery: verifies all eight tools are registered.
- Tool execution: bootstrap, sync, status, search, read, architecture context, change validation, and ADR proposal.
- MCP resources: reads both project status and architecture context.
- File safety: rejects path traversal and secret-file reads.
- Indexer safety: excludes secrets, internal snapshot files, and symlinks outside the project root.
- Snapshot behavior: verifies stable hashes and change detection.

## Manual host integration

After CI passes, configure Codex with `integrations/codex-config.toml.example` (replace absolute paths) or use the command in README. Restart Codex and run `/mcp`. A successful local test requires the host to list all eight tools.

Copy `integrations/AGENTS.md` to the root of the Nexus SaaS repository. This file tells the agent to bootstrap at session start and sync after edits.

## What this does not prove

A passing CI run does not prove production reliability, complete secret detection, semantic correctness, or zero-crash behavior. Validate with the actual Nexus SaaS checkout and the intended AI host before production use.
