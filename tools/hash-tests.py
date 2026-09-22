#!/usr/bin/env python3
"""Compute (and optionally update) the protected-file hash for a sample.

The hash covers everything an agent could use to change what "pytest passes"
means: every file under tests/, plus any pytest configuration at the sample
root. It deliberately does NOT cover src/ — that is what the agent is supposed
to change.

The digest is over sorted POSIX-relative paths and their file bytes, so it is
stable across machines and independent of filesystem ordering.

    python3 tools/hash-tests.py samples/001-easy-receipt-totals
    python3 tools/hash-tests.py --update samples/001-easy-receipt-totals
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT_CONFIG = ("conftest.py", "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini")
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache"}
EXCLUDE_SUFFIX = {".pyc", ".pyo"}


def protected_files(sample: Path) -> list[Path]:
    found = []
    tests = sample / "tests"
    if tests.is_dir():
        for p in tests.rglob("*"):
            if not p.is_file():
                continue
            if EXCLUDE_DIRS & set(p.relative_to(sample).parts):
                continue
            if p.suffix in EXCLUDE_SUFFIX:
                continue
            found.append(p)
    for name in ROOT_CONFIG:
        p = sample / name
        if p.is_file():
            found.append(p)
    return sorted(found, key=lambda p: p.relative_to(sample).as_posix())


def digest(sample: Path) -> str:
    h = hashlib.sha256()
    files = protected_files(sample)
    if not files:
        sys.exit(f"error: no protected files found under {sample}")
    for p in files:
        rel = p.relative_to(sample).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        h.update(hashlib.sha256(p.read_bytes()).hexdigest().encode())
        h.update(b"\n")
    return h.hexdigest()


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--update"]
    update = "--update" in sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    sample = Path(args[0]).resolve()
    if not sample.is_dir():
        sys.exit(f"error: not a directory: {sample}")
    d = digest(sample)
    if update:
        manifest = sample / "manifest.yaml"
        text = manifest.read_text()
        new, n = re.subn(r"(?m)^tests_sha256:.*$", f"tests_sha256: {d}", text)
        if n != 1:
            sys.exit(f"error: expected exactly one tests_sha256 line in {manifest}, found {n}")
        manifest.write_text(new)
        print(f"updated {manifest.name}: {d}")
    else:
        print(d)


if __name__ == "__main__":
    main()
