from pathlib import Path

GOVERNANCE_FILES = [
    "governance/PRODUCT_CONSTITUTION.md",
    "governance/ARCHITECTURE_CONSTITUTION.md",
    "governance/AI_CODING_RULES.md",
    "governance/ENTERPRISE_QUALITY_GATES.md",
]

def _read_files(root: Path, paths: list[str]) -> str:
    chunks = []
    for rel in paths:
        p = root / rel
        if p.is_file():
            chunks.append(f"## {rel}\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks) or "No governance documents found. Status: UNKNOWN."

def read_governance(repo_root: Path) -> str:
    return _read_files(repo_root, GOVERNANCE_FILES)

def read_blueprint(repo_root: Path) -> str:
    return _read_files(repo_root, [
        "governance/BUILD_BLUEPRINT.md",
        "governance/MODULE_CONTRACT_TEMPLATE.md",
        "governance/ENTERPRISE_QUALITY_GATES.md",
    ])

def read_decisions(repo_root: Path) -> str:
    return _read_files(repo_root, ["governance/DECISION_REGISTER.md"])

def validate_change(summary: str, touched_paths: list[str]) -> list[str]:
    findings = []
    text = (summary + " " + " ".join(touched_paths)).lower()
    checks = [
        (("tenant", "tenant_id", "rls"), "Multi-tenancy changes must preserve tenant isolation and authorization tests."),
        (("migration", "schema", "database"), "Database changes require a reversible migration and compatibility review."),
        (("module", "plugin", "registry"), "Dynamic module changes must preserve lifecycle contracts and dependency validation."),
        (("auth", "permission", "role"), "Authorization changes require deny-by-default behavior and permission tests."),
        (("secret", ".env", "credential"), "Do not commit secrets or credential material."),
        (("billing", "subscription", "invoice", "payment"), "Billing changes require idempotency, auditability, and reconciliation tests."),
        (("backup", "restore", "disaster", "recovery"), "Recovery changes require restore drills and documented RPO/RTO evidence."),
        (("event", "webhook", "queue", "outbox"), "Asynchronous integration changes require idempotency, retry, ordering, and dead-letter tests."),
    ]
    for terms, message in checks:
        if any(term in text for term in terms):
            findings.append(message)
    return findings
