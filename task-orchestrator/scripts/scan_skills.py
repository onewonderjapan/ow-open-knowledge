#!/usr/bin/env python3
"""Discover Codex skills and classify them without executing their contents."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


VALID_SCOPES = {"project", "user", "admin", "plugin", "system"}
PROTECTED_SCOPES = {"admin", "plugin", "system"}
DEFAULT_RULES = Path(__file__).resolve().parent.parent / "references" / "category-rules.yaml"


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        quote = value[0]
        if quote == '"':
            try:
                return str(json.loads(value)).strip()
            except json.JSONDecodeError:
                pass
        value = value[1:-1].replace("''", "'")
    return value.strip()


def _frontmatter_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]
    raise ValueError("missing closing YAML frontmatter delimiter")


def parse_skill(path: Path) -> dict[str, str]:
    """Return name and description from the first YAML frontmatter block."""
    lines = _frontmatter_lines(path)
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if key not in {"name", "description"}:
            index += 1
            continue
        if raw_value in {">", "|", ">-", "|-", ">+", "|+"}:
            style = raw_value[0]
            block: list[str] = []
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[:1].isspace():
                    break
                block.append(candidate.strip())
                index += 1
            if style == ">":
                values[key] = " ".join(part for part in block if part).strip()
            else:
                values[key] = "\n".join(block).strip()
            continue
        values[key] = _unquote(raw_value)
        index += 1

    for required in ("name", "description"):
        if not values.get(required):
            raise ValueError(f"missing non-empty {required!r} in YAML frontmatter")
    return {"name": values["name"], "description": values["description"]}


def load_category_rules(path: Path) -> dict[str, list[str]]:
    """Parse the constrained categories-to-string-list YAML format."""
    lines = path.read_text(encoding="utf-8").splitlines()
    rules: dict[str, list[str]] = {}
    in_categories = False
    current: str | None = None
    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent == 0:
            if stripped != "categories:":
                raise ValueError(f"line {line_number}: expected 'categories:'")
            in_categories = True
            current = None
            continue
        if not in_categories:
            raise ValueError(f"line {line_number}: category before 'categories:'")
        if indent == 2 and stripped.endswith(":"):
            current = stripped[:-1].strip().lower()
            if not current:
                raise ValueError(f"line {line_number}: empty category name")
            rules.setdefault(current, [])
            continue
        if indent == 4 and stripped.startswith("- ") and current:
            signal = _unquote(stripped[2:]).lower()
            if not signal:
                raise ValueError(f"line {line_number}: empty category signal")
            rules[current].append(signal)
            continue
        raise ValueError(f"line {line_number}: unsupported category rule syntax")
    if not rules:
        raise ValueError("no category rules found")
    return rules


def _signal_matches(haystack: str, signal: str) -> bool:
    pattern = rf"(?<![a-z0-9]){re.escape(signal)}(?![a-z0-9])"
    return re.search(pattern, haystack) is not None


def _categories_for(
    metadata: dict[str, str], path: Path, rules: dict[str, list[str]]
) -> list[str]:
    haystack = " ".join(
        (metadata["name"].lower(), metadata["description"].lower(), str(path).lower())
    )
    matches = [
        category
        for category, signals in rules.items()
        if any(_signal_matches(haystack, signal) for signal in signals)
    ]
    return sorted(matches) or ["other"]


def _skill_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    if root.is_file():
        return [root] if root.name == "SKILL.md" else []
    direct = root / "SKILL.md"
    found = list(root.rglob("SKILL.md"))
    if direct.is_file() and direct not in found:
        found.append(direct)
    return sorted(found, key=lambda item: str(item))


def scan_roots(
    roots: list[tuple[str, Path]], rules: dict[str, list[str]]
) -> dict[str, object]:
    """Return stable, sorted skill records and non-fatal warnings."""
    skills: list[dict[str, object]] = []
    warnings: list[dict[str, str]] = []
    seen: set[Path] = set()

    for scope, root in roots:
        if scope not in VALID_SCOPES:
            raise ValueError(f"unsupported scope: {scope}")
        for skill_file in _skill_files(Path(root)):
            resolved = skill_file.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                metadata = parse_skill(resolved)
            except (OSError, UnicodeError, ValueError) as error:
                warnings.append({"path": str(resolved), "error": str(error)})
                continue
            skills.append(
                {
                    "name": metadata["name"],
                    "description": metadata["description"],
                    "skill_file": str(resolved),
                    "scope": scope,
                    "writable": scope not in PROTECTED_SCOPES,
                    "categories": _categories_for(metadata, resolved, rules),
                }
            )

    skills.sort(key=lambda item: (str(item["name"]), str(item["scope"]), str(item["skill_file"])))
    warnings.sort(key=lambda item: item["path"])
    return {"skills": skills, "warnings": warnings}


def _git_root(cwd: Path) -> Path:
    completed = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 0 and completed.stdout.strip():
        return Path(completed.stdout.strip()).resolve()
    return cwd.resolve()


def _project_skill_roots(cwd: Path, project_root: Path) -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    current = cwd.resolve()
    while True:
        roots.append(("project", current / ".agents" / "skills"))
        if current == project_root or current.parent == current:
            break
        current = current.parent
    return roots


def build_default_roots(cwd: Path) -> tuple[Path, list[tuple[str, Path]]]:
    """Resolve project, user, compatibility, admin, plugin, and system roots."""
    cwd = cwd.resolve()
    project_root = _git_root(cwd)
    roots = _project_skill_roots(cwd, project_root)

    user_home = Path.home()
    roots.append(("user", user_home / ".agents" / "skills"))

    codex_home = Path(os.environ.get("CODEX_HOME", user_home / ".codex")).expanduser()
    compatibility_skills = codex_home / "skills"
    if compatibility_skills.is_dir():
        for child in sorted(compatibility_skills.iterdir(), key=lambda item: item.name):
            if not child.is_dir():
                continue
            roots.append(("system" if child.name == ".system" else "user", child))

    admin_root = Path("/etc/codex/skills")
    if admin_root.exists():
        roots.append(("admin", admin_root))

    plugin_cache = codex_home / "plugins" / "cache"
    if plugin_cache.is_dir():
        plugin_roots = sorted(
            (path for path in plugin_cache.rglob("skills") if path.is_dir()),
            key=lambda item: str(item),
        )
        roots.extend(("plugin", path) for path in plugin_roots)

    return project_root, roots


def _root_spec(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("root must use SCOPE=PATH")
    scope, raw_path = value.split("=", 1)
    scope = scope.strip().lower()
    if scope not in VALID_SCOPES:
        raise argparse.ArgumentTypeError(
            f"scope must be one of: {', '.join(sorted(VALID_SCOPES))}"
        )
    if not raw_path.strip():
        raise argparse.ArgumentTypeError("root path cannot be empty")
    return scope, Path(raw_path).expanduser()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--root", action="append", type=_root_spec, default=[])
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        rules = load_category_rules(args.rules)
        project_root, roots = build_default_roots(args.cwd)
        roots.extend(args.root)
        catalog = scan_roots(roots, rules)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"scan-skills: {error}", file=sys.stderr)
        return 2

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        **catalog,
    }
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=False,
        indent=2 if args.pretty else None,
        sort_keys=False,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
