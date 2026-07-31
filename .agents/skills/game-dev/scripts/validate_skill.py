#!/usr/bin/env python3
"""Validate the game-dev skill package without third-party dependencies."""

from __future__ import annotations

import csv
import py_compile
import re
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skill_file = root / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        frontmatter = ""
    else:
        parts = text.split("---", 2)
        frontmatter = parts[1] if len(parts) == 3 else ""
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if fields.get("name") != "game-dev":
        errors.append("frontmatter name must be game-dev")
    description = fields.get("description", "")
    if len(description) < 80:
        errors.append("description is too vague to trigger reliably")
    for term in ("Blender", "Unity", "Three.js"):
        if term not in description:
            errors.append(f"description must mention {term}")

    required = [
        "references/airbourne-arena.md",
        "references/web-runtime.md",
        "references/blender-pipeline.md",
        "references/unity-lane.md",
        "references/release-gates.md",
        "scripts/audit_glb.py",
        "scripts/audit_blender_scene.py",
        "evals/prompts.csv",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"missing required skill resource: {relative}")

    mentioned = set(
        re.findall(r"`((?:references|scripts)/[^`]+)`", text)
    )
    for relative in sorted(mentioned):
        if not (root / relative).is_file():
            errors.append(f"SKILL.md references missing resource: {relative}")

    for path in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{path.name} does not compile: {exc}")

    eval_path = root / "evals" / "prompts.csv"
    with eval_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 8:
        errors.append("eval set must contain at least eight prompts")
    if not any(row.get("should_trigger") == "true" for row in rows):
        errors.append("eval set has no positive trigger cases")
    if not any(row.get("should_trigger") == "false" for row in rows):
        errors.append("eval set has no negative controls")
    for row_number, row in enumerate(rows, start=2):
        if row.get("should_trigger") not in {"true", "false"}:
            errors.append(f"eval row {row_number} has invalid should_trigger")
        if not row.get("prompt") or not row.get("expected_behavior"):
            errors.append(f"eval row {row_number} is incomplete")

    text_suffixes = {".md", ".py", ".csv"}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in text_suffixes:
            body = path.read_text(encoding="utf-8")
            if "UNRESOLVED_SKILL_PLACEHOLDER" in body:
                errors.append(
                    f"unresolved content placeholder in {path.relative_to(root)}"
                )

    if errors:
        print("game-dev skill validation: FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        "game-dev skill validation: PASS "
        f"({len(rows)} eval prompts, {len(required)} required resources)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
