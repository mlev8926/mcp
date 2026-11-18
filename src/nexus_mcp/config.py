from dataclasses import dataclass
from pathlib import Path
import os

PACKAGE_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Settings:
    governance_root: Path
    workspace_root: Path | None
    max_file_bytes: int = 500_000

def load_settings() -> Settings:
    # Legacy NEXUS_PROJECT_ROOT is accepted as the governance root only.
    governance_value = (
        os.environ.get("NEXUS_GOVERNANCE_ROOT")
        or os.environ.get("NEXUS_PROJECT_ROOT")
        or str(PACKAGE_REPOSITORY_ROOT)
    )
    governance_root = Path(governance_value).expanduser().resolve()
    if not governance_root.exists() or not governance_root.is_dir():
        raise RuntimeError(f"NEXUS_GOVERNANCE_ROOT is not a directory: {governance_root}")

    workspace_value = os.environ.get("NEXUS_WORKSPACE_ROOT", "").strip()
    workspace_root = Path(workspace_value).expanduser().resolve() if workspace_value else None
    if workspace_root is not None:
        if not workspace_root.exists() or not workspace_root.is_dir():
            raise RuntimeError(
                "NEXUS_WORKSPACE_ROOT must point to an existing directory. "
                "Leave it unset until the Nexus SaaS workspace is created."
            )
        if workspace_root == governance_root:
            raise RuntimeError("Governance root and development workspace must be separate.")

    return Settings(
        governance_root=governance_root,
        workspace_root=workspace_root,
    )
