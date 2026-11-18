import ast
import importlib
import json
import sys

import pytest
from mcp import Client

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def server_module(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_PROJECT_ROOT", str(tmp_path))
    (tmp_path / "governance").mkdir()
    (tmp_path / "governance" / "ARCHITECTURE_CONSTITUTION.md").write_text(
        "# Test Constitution\\nStatus: APPROVED DESIGN\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "AI_CODING_RULES.md").write_text(
        "# Test Rules\\nCall bootstrap first.\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "PRODUCT_CONSTITUTION.md").write_text(
        "# Product Direction\\nSaaS and on-premise.\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "BUILD_BLUEPRINT.md").write_text(
        "# Build Blueprint\\nBuild from zero.\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "DECISION_REGISTER.md").write_text(
        "# Decisions\\nAPPROVED product model.\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "ENTERPRISE_QUALITY_GATES.md").write_text(
        "# Quality Gates\\nSecurity and reliability.\\n", encoding="utf-8"
    )
    (tmp_path / "app.py").write_text("VALUE = 'nexus-test-marker'\\n", encoding="utf-8")
    sys.modules.pop("nexus_mcp.server", None)
    return importlib.import_module("nexus_mcp.server")

def payload(result):
    data = result.structured_content
    if data is not None:
        if isinstance(data, dict) and "result" in data:
            return data["result"]
        return data
    for block in result.content:
        text = getattr(block, "text", None)
        if text is None:
            continue
        try:
            return json.loads(text)
        except (TypeError, json.JSONDecodeError):
            try:
                return ast.literal_eval(text)
            except (ValueError, SyntaxError):
                return text
    return None

@pytest.mark.anyio
async def test_all_eight_tools_and_two_resources(server_module, tmp_path):
    async with Client(server_module.mcp, raise_exceptions=True) as client:
        listed = await client.list_tools()
        names = {tool.name for tool in listed.tools}
        expected = {
            "nexus_bootstrap_context", "nexus_sync_project_context",
            "nexus_project_status", "nexus_search_project",
            "nexus_read_project_file", "nexus_get_architecture_context",
            "nexus_validate_change", "nexus_propose_adr",
            "nexus_get_build_blueprint", "nexus_get_decision_register",
            "nexus_get_workspace_status",
        }
        assert names == expected

        status_result = await client.call_tool("nexus_project_status", {})
        status = payload(status_result)
        assert status is not None, status_result.model_dump()
        assert status["governance_ready"] is True
        assert status["workspace_configured"] is False
        assert status["workspace_state"] == "NOT_CREATED_OR_NOT_CONFIGURED"
        assert status["file_count"] >= 3

        bootstrap = payload(await client.call_tool("nexus_bootstrap_context", {}))
        assert "APPROVED DESIGN" in bootstrap["governance"]
        assert bootstrap["file_count"] >= 3

        search = payload(await client.call_tool(
            "nexus_search_project", {"query": "nexus-test-marker"}
        ))
        assert any(item["path"] == "app.py" for item in search)

        read = payload(await client.call_tool(
            "nexus_read_project_file", {"path": "app.py"}
        ))
        assert "nexus-test-marker" in read

        architecture = payload(await client.call_tool("nexus_get_architecture_context", {}))
        assert "Test Constitution" in architecture

        blueprint = payload(await client.call_tool("nexus_get_build_blueprint", {}))
        assert "Build Blueprint" in blueprint

        decisions = payload(await client.call_tool("nexus_get_decision_register", {}))
        assert "APPROVED product model" in decisions

        workspace = payload(await client.call_tool("nexus_get_workspace_status", {}))
        assert workspace["configured"] is False

        validation = payload(await client.call_tool(
            "nexus_validate_change",
            {"summary": "change tenant RLS", "touched_paths": ["db/schema.sql"]},
        ))
        assert validation["status"] == "REVIEW_REQUIRED"
        assert len(validation["findings"]) >= 2

        proposal_path = payload(await client.call_tool(
            "nexus_propose_adr",
            {
                "title": "Test module lifecycle",
                "context": "Need a test decision.",
                "decision": "Keep lifecycle explicit.",
                "consequences": "Add contract tests.",
            },
        ))
        assert proposal_path.startswith("governance/adr/proposals/")
        assert (tmp_path / proposal_path).is_file()

        (tmp_path / "new_feature.py").write_text("NEW_FEATURE = True\\n", encoding="utf-8")
        sync = payload(await client.call_tool("nexus_sync_project_context", {}))
        assert "new_feature.py" in sync["added"]

        for uri in (
            "nexus://project/status", "nexus://architecture/context",
            "nexus://blueprint/build", "nexus://governance/decisions",
        ):
            resource = await client.read_resource(uri)
            assert resource.contents

@pytest.mark.anyio
async def test_read_tool_rejects_path_traversal_and_secret_files(server_module, tmp_path):
    (tmp_path.parent / "outside-nexus-secret.txt").write_text("do-not-read", encoding="utf-8")
    (tmp_path / ".env.production").write_text("TOKEN=do-not-read", encoding="utf-8")
    async with Client(server_module.mcp, raise_exceptions=True) as client:
        traversal = await client.call_tool(
            "nexus_read_project_file", {"path": "../outside-nexus-secret.txt"}
        )
        secret = await client.call_tool(
            "nexus_read_project_file", {"path": ".env.production"}
        )
        assert traversal.is_error is True
        assert secret.is_error is True

@pytest.mark.anyio
async def test_real_stdio_subprocess_transport(tmp_path):
    from pathlib import Path
    import os
    import sys
    from mcp import StdioServerParameters

    (tmp_path / "governance").mkdir()
    (tmp_path / "governance" / "ARCHITECTURE_CONSTITUTION.md").write_text(
        "# Stdio Test\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "AI_CODING_RULES.md").write_text(
        "# Agent Rules\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "PRODUCT_CONSTITUTION.md").write_text(
        "# Product Direction\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "BUILD_BLUEPRINT.md").write_text(
        "# Build Blueprint\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "DECISION_REGISTER.md").write_text(
        "# Decisions\\n", encoding="utf-8"
    )
    (tmp_path / "governance" / "ENTERPRISE_QUALITY_GATES.md").write_text(
        "# Quality Gates\\n", encoding="utf-8"
    )
    project_dir = Path(__file__).resolve().parents[1]
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "nexus_mcp.server"],
        env={"NEXUS_PROJECT_ROOT": str(tmp_path)},
        cwd=str(project_dir),
    )
    async with Client(server) as client:
        assert client.instructions and "nexus_bootstrap_context" in client.instructions
        listed = await client.list_tools()
        assert len(listed.tools) == 11
        status = await client.call_tool("nexus_project_status", {})
        assert status.is_error is False
        status_data = payload(status)
        assert status_data["governance_ready"] is True
