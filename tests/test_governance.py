from nexus_mcp.governance import validate_change

def test_tenant_change_requires_isolation_review():
    findings = validate_change("add tenant settings", ["app/models/tenant.py"])
    assert any("tenant isolation" in item for item in findings)

def test_plain_ui_change_has_no_rule_trigger():
    assert validate_change("adjust button spacing", ["web/button.tsx"]) == []
