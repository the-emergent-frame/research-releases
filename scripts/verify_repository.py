#!/usr/bin/env python3
"""Verify frozen PDF hashes and run every paper-specific numerical check."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ("TEF-2026-001", "TEF-2026-002")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    for paper_id in PAPERS:
        paper_root = ROOT / "papers" / paper_id
        manifest = json.loads((paper_root / "metadata" / "release.json").read_text())
        for artifact_name in ("pdf", "source"):
            artifact = manifest[artifact_name]
            artifact_path = paper_root / artifact["path"]
            actual_hash = sha256(artifact_path)
            expected_hash = artifact["sha256"]
            if actual_hash != expected_hash:
                raise SystemExit(f"{paper_id}: {artifact_name} SHA-256 mismatch: {actual_hash}")

        subprocess.run(
            [sys.executable, str(paper_root / "calculations" / "verify.py")],
            cwd=paper_root,
            check=True,
        )
        print(f"{paper_id}: source/PDF hashes and numerical checks verified")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
