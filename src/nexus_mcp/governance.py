from pathlib import Path

GOVERNANCE_FILES = [
    "governance/ARCHITECTURE_CONSTITUTION.md",
    "governance/AI_CODING_RULES.md",
]

def read_governance(repo_root: Path) -> str:
    chunks = []
    for rel in GOVERNANCE_FILES:
        p = repo_root / rel
        if p.is_file():
            chunks.append(f"## {rel}\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks) or "No governance documents found. Architecture status: UNKNOWN."

def validate_change(summary: str, touched_paths: list[str]) -> list[str]:
    findings = []
    text = (summary + " " + " ".join(touched_paths)).lower()
    checks = [
        (("tenant", "tenant_id", "rls"), "Multi-tenancy changes must preserve tenant isolation and authorization tests."),
        (("migration", "schema", "database"), "Database changes require a reversible migration and compatibility review."),
        (("module", "plugin", "registry"), "Dynamic module changes must preserve lifecycle contracts and dependency validation."),
        (("auth", "permission", "role"), "Authorization changes require deny-by-default behavior and permission tests."),
        (("secret", ".env", "credential"), "Do not commit secrets or credential material."),
    ]
    for terms, message in checks:
        if any(term in text for term in terms):
            findings.append(message)
    return findings
