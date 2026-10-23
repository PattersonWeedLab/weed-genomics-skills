#!/usr/bin/env python3
"""Install the canonical skill without overwriting existing user content."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git_value(root, *args):
    if not (root / ".git").exists():
        return None  # An archive nested in another checkout is not that checkout.
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def install(root, destination):
    root = Path(root).resolve()
    destination = Path(destination).expanduser().absolute()
    source = root / "skills/weed-genomics"
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Destination exists; review and archive it explicitly before updating: {destination}")
    if destination.resolve().is_relative_to(root):
        raise ValueError("Install outside the source checkout; keep one canonical skill in the repository")
    for path in [source, *source.rglob("*"), root / "LICENSE"]:
        if path.is_symlink():
            raise ValueError(f"Refusing symlink in distributable content: {path.relative_to(root)}")
    if not (source / "SKILL.md").is_file() or not (root / "LICENSE").is_file():
        raise ValueError("Missing canonical skill or LICENSE")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Exclusive: never overwrite even an empty installation.
    try:
        shutil.copytree(source, destination, dirs_exist_ok=True)
        shutil.copy2(root / "LICENSE", destination / "LICENSE")
        commit = git_value(root, "rev-parse", "HEAD")
        status = git_value(root, "status", "--porcelain", "--untracked-files=all")
        hashes = {p.relative_to(destination).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(destination.rglob("*")) if p.is_file()}
        manifest = {"repository": "https://github.com/PattersonWeedLab/weed-genomics-skills",
                    "commit": commit, "dirty": None if status is None else bool(status),
                    "sha256": hashes}
        (destination / "INSTALLATION.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest
    except Exception:
        # Only this invocation's newly-created, incomplete deployment is removed.
        shutil.rmtree(destination)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--client", choices=("codex", "claude"))
    group.add_argument("--dest", type=Path, help="explicit destination directory outside this checkout")
    args = parser.parse_args()
    destination = args.dest or Path.home() / (".agents" if args.client == "codex" else ".claude") / "skills/weed-genomics"
    try:
        manifest = install(ROOT, destination)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Install failed: {exc}\n")
    print(f"Installed {len(manifest['sha256'])} files to {destination}")
    print(f"Source commit: {manifest['commit'] or 'unknown'}; dirty: {manifest['dirty']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
