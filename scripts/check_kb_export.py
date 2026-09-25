#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`knowledge-notes/` が非公開 KB の exporter 出力のままかを検証する（標準ライブラリのみ）。

usage:
  python3 scripts/check_kb_export.py           # リポジトリ直下の knowledge-notes/
  python3 scripts/check_kb_export.py path/to/repo

`knowledge-notes/` は非公開リポジトリ onewonderjapan/knowledge-base の
`scripts/kb.py export-public` だけが生成する。手編集や、脱敏前の内容の混入を
防ぐための門番。ディレクトリがまだ無ければ何もせず 0 で終わる。

検証内容:
- `knowledge-notes/` 自体・中身のどれもシンボリックリンクではない
- `manifest.json` のスキーマ（generator / source_repo / source_commit /
  exported_at / count / scrub_patterns（3 件以上）/ notes / files）
- 直下の README.md / INDEX.md は `files` に、それ以外の全 `*.md` は `notes` に載り、
  sha256 が一致する。載っているパスは全て実在し、count も一致する。
  manifest.json 以外の非 md ファイルは不可。全ファイル strict UTF-8（BOM なし）
- 各ノートの frontmatter: `scope: public`、`source: knowledge-base@...`、
  `id` が manifest と一致、`type` が `digest` ではない
- ノート・README.md・INDEX.md が manifest の scrub_patterns にも、下の DENYLIST にも当たらない
- manifest.json 自体（`scrub_patterns` の値を除く全キー・全文字列）も同じく検査する
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

NOTES_DIR = "knowledge-notes"
MANIFEST = "manifest.json"
INDEX_FILES = {"README.md", "INDEX.md"}
MIN_SCRUB_PATTERNS = 3
GENERATOR = "scripts/kb.py export-public"
SOURCE_REPO = "onewonderjapan/knowledge-base"
SOURCE_PREFIX = "knowledge-base@"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s+-\s*(.*)$")

# 内部パス・内部構成の断片。exporter の scrub_patterns が差し替えられても、
# これだけは公開物に出てはいけない（大文字小文字は区別しない）。
DENYLIST = (
    "/home/baibai",
    "172.72.",
    "C:\\",
    "~/Base",
    "~/outbox",
    "lab_inputs/",
    "orchestration/",
)


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict:
    """単純な `key: scalar` / `key: [a, b]` / ブロックリストだけを読む最小パーサ。

    frontmatter が無い・閉じていない・解釈できない行があれば ValueError。
    """
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        raise ValueError("frontmatter がありません（1 行目が `---` ではない）")
    fields: dict = {}
    current = None
    for raw in lines[1:]:
        line = raw.rstrip("\r")
        if line == "---":
            return fields
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = LIST_ITEM_RE.match(line)
        if item and current is not None and isinstance(fields[current], list):
            fields[current].append(_unquote(item.group(1)))
            continue
        match = KEY_RE.match(line)
        if not match:
            raise ValueError(f"frontmatter の行を解釈できません: {line!r}")
        key, value = match.group(1), match.group(2).strip()
        if not value:
            fields[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fields[key] = [_unquote(v) for v in inner.split(",")] if inner else []
        else:
            fields[key] = _unquote(value)
        current = key
    raise ValueError("frontmatter が閉じていません（`---` が無い）")


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def denylist_hits(text: str) -> list[str]:
    hits = []
    folded = text.casefold()
    for term in DENYLIST:
        index = folded.find(term.casefold())
        if index != -1:
            hits.append(f"{_line_of(text, index)} 行目: 禁止語 {term!r}")
    return hits


def scrub_hits(text: str, patterns: list) -> list[str]:
    hits = []
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            hits.append(
                f"{_line_of(text, match.start())} 行目: scrub_pattern {pattern.pattern!r} に一致 "
                f"({match.group(0)!r})"
            )
    return hits


def _check_manifest_schema(manifest, problems: list[str]):
    """スキーマ違反を problems に積み、使える scrub_patterns / notes / files を返す。"""
    if not isinstance(manifest, dict):
        problems.append(f"{MANIFEST}: トップレベルがオブジェクトではありません")
        return [], [], []
    if manifest.get("generator") != GENERATOR:
        problems.append(f"{MANIFEST}: generator は {GENERATOR!r} であるべき: {manifest.get('generator')!r}")
    if manifest.get("source_repo") != SOURCE_REPO:
        problems.append(
            f"{MANIFEST}: source_repo は {SOURCE_REPO!r} であるべき: {manifest.get('source_repo')!r}"
        )
    commit = manifest.get("source_commit")
    if not isinstance(commit, str) or not commit.strip():
        problems.append(f"{MANIFEST}: source_commit が空か文字列ではありません: {commit!r}")
    exported = manifest.get("exported_at")
    valid_date = isinstance(exported, str) and bool(DATE_RE.match(exported))
    if valid_date:
        try:
            datetime.date.fromisoformat(exported)
        except ValueError:
            valid_date = False
    if not valid_date:
        problems.append(f"{MANIFEST}: exported_at は YYYY-MM-DD であるべき: {exported!r}")
    count = manifest.get("count")
    if not isinstance(count, int) or isinstance(count, bool):
        problems.append(f"{MANIFEST}: count が整数ではありません: {count!r}")

    patterns = []
    raw_patterns = manifest.get("scrub_patterns")
    if not isinstance(raw_patterns, list):
        problems.append(f"{MANIFEST}: scrub_patterns が配列ではありません")
    elif len(raw_patterns) < MIN_SCRUB_PATTERNS:
        problems.append(
            f"{MANIFEST}: scrub_patterns は {MIN_SCRUB_PATTERNS} 件以上必要（{len(raw_patterns)} 件）"
            "。空の scrub で export された可能性"
        )
    if isinstance(raw_patterns, list):
        for raw in raw_patterns:
            if not isinstance(raw, str) or not raw:
                problems.append(f"{MANIFEST}: scrub_patterns に文字列でない要素: {raw!r}")
                continue
            try:
                patterns.append(re.compile(raw))
            except re.error as error:
                problems.append(f"{MANIFEST}: scrub_pattern {raw!r} が正規表現として不正 ({error})")

    files = []
    raw_files = manifest.get("files")
    if not isinstance(raw_files, list):
        problems.append(f"{MANIFEST}: files が配列ではありません（README.md / INDEX.md の sha256 が必要）")
    else:
        for position, entry in enumerate(raw_files):
            keys = ("path", "sha256")
            if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry.get(k) for k in keys):
                problems.append(f"{MANIFEST}: files[{position}] に path / sha256 の文字列がありません: {entry!r}")
                continue
            files.append(entry)
        paths = sorted(entry["path"] for entry in files)
        if paths != sorted(INDEX_FILES):
            problems.append(f"{MANIFEST}: files はちょうど {sorted(INDEX_FILES)} を載せるべき: {paths}")

    notes = []
    raw_notes = manifest.get("notes")
    if not isinstance(raw_notes, list):
        problems.append(f"{MANIFEST}: notes が配列ではありません")
        return patterns, notes, files
    for position, entry in enumerate(raw_notes):
        keys = ("id", "path", "sha256")
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry.get(k) for k in keys):
            problems.append(f"{MANIFEST}: notes[{position}] に id / path / sha256 の文字列がありません: {entry!r}")
            continue
        notes.append(entry)
    if isinstance(count, int) and not isinstance(count, bool) and count != len(raw_notes):
        problems.append(f"{MANIFEST}: count={count} だが notes は {len(raw_notes)} 件")
    return patterns, notes, files


def _manifest_strings(value, where: str = "$"):
    """manifest の全キー・全文字列を (JSON パス, 文字列) で列挙する。"""
    if isinstance(value, dict):
        for key, child in value.items():
            yield f"{where} のキー", str(key)
            yield from _manifest_strings(child, f"{where}.{key}")
    elif isinstance(value, list):
        for position, child in enumerate(value):
            yield from _manifest_strings(child, f"{where}[{position}]")
    elif isinstance(value, str):
        yield where, value


def _read_exported(path: Path, shown: str, expected_sha: str, problems: list[str]):
    """sha256 を照合し、strict UTF-8（BOM なし）で読む。読めなければ None（fail closed）。"""
    data = path.read_bytes()
    expected = expected_sha.lower()
    if not SHA256_RE.match(expected):
        problems.append(f"{shown}: manifest の sha256 が 64 桁の16進ではありません: {expected_sha!r}")
    elif hashlib.sha256(data).hexdigest() != expected:
        problems.append(f"{shown}: sha256 が manifest と一致しません（export 後に手編集された）")
    if data.startswith(b"\xef\xbb\xbf"):
        problems.append(f"{shown}: BOM 付きです（UTF-8 BOM なしであるべき）")
        data = data[3:]
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        problems.append(f"{shown}: UTF-8 として読めません ({error})")
        return None


def check(root: Path) -> list[str]:
    notes_dir = root / NOTES_DIR
    if notes_dir.is_symlink():
        return [f"{NOTES_DIR}/: ディレクトリ自体がシンボリックリンクです（実体を置くこと）"]
    if not notes_dir.exists():
        return []
    problems: list[str] = []

    def rel(path: Path) -> str:
        return path.relative_to(notes_dir).as_posix()

    files = sorted(p for p in notes_dir.rglob("*") if p.is_file() or p.is_symlink())
    for path in files:
        if path.is_symlink():
            problems.append(f"{NOTES_DIR}/{rel(path)}: シンボリックリンクは置けません")
    files = [p for p in files if not p.is_symlink()]
    on_disk = {rel(p): p for p in files}

    manifest_path = notes_dir / MANIFEST
    if MANIFEST not in on_disk:
        problems.append(f"{NOTES_DIR}/{MANIFEST}: ありません（exporter 以外で作られたディレクトリ）")
        for name in sorted(INDEX_FILES & on_disk.keys()):
            text = on_disk[name].read_text(encoding="utf-8", errors="replace")
            problems.extend(f"{NOTES_DIR}/{name}: {hit}" for hit in denylist_hits(text))
        return problems
    try:
        manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        problems.append(f"{NOTES_DIR}/{MANIFEST}: JSON として読めません ({error})")
        return problems
    schema_problems: list[str] = []
    patterns, notes, index_entries = _check_manifest_schema(manifest, schema_problems)
    problems.extend(f"{NOTES_DIR}/{p}" for p in schema_problems)

    # manifest 自体も公開物。scrub_patterns の値（検出語そのもの）だけは除いて検査する。
    if isinstance(manifest, dict):
        scanned = {k: v for k, v in manifest.items() if k != "scrub_patterns"}
        for where, value in _manifest_strings(scanned):
            for hit in denylist_hits(value) + scrub_hits(value, patterns):
                problems.append(f"{NOTES_DIR}/{MANIFEST}: {where}: {hit.split(': ', 1)[1]}")

    listed: dict[str, dict] = {}
    seen_ids: set[str] = set()
    for entry in notes:
        path_str = entry["path"]
        pure = PurePosixPath(path_str)
        if pure.is_absolute() or ".." in pure.parts or "\\" in path_str or path_str != pure.as_posix():
            problems.append(f"{NOTES_DIR}/{MANIFEST}: 不正なパス {path_str!r}（{NOTES_DIR}/ からの相対 POSIX パス）")
            continue
        if pure.suffix != ".md" or path_str in INDEX_FILES:
            problems.append(f"{NOTES_DIR}/{MANIFEST}: ノートでないパスが載っています: {path_str!r}")
            continue
        if path_str in listed:
            problems.append(f"{NOTES_DIR}/{MANIFEST}: パスが重複しています: {path_str!r}")
            continue
        if entry["id"] in seen_ids:
            problems.append(f"{NOTES_DIR}/{MANIFEST}: id が重複しています: {entry['id']!r}")
        seen_ids.add(entry["id"])
        listed[path_str] = entry

    for name, path in on_disk.items():
        if name == MANIFEST or name in INDEX_FILES:
            continue
        if not name.endswith(".md"):
            problems.append(f"{NOTES_DIR}/{name}: manifest.json 以外の非 Markdown ファイルは置けません")
        elif name not in listed:
            problems.append(f"{NOTES_DIR}/{name}: manifest に載っていません（手で追加されたノート）")
            text = path.read_text(encoding="utf-8", errors="replace")
            problems.extend(f"{NOTES_DIR}/{name}: {hit}" for hit in denylist_hits(text))

    # README.md / INDEX.md: manifest.files の sha256、strict UTF-8、scrub_patterns + DENYLIST。
    index_listed = {entry["path"]: entry for entry in index_entries if entry["path"] in INDEX_FILES}
    for name in sorted(INDEX_FILES):
        shown = f"{NOTES_DIR}/{name}"
        path = on_disk.get(name)
        entry = index_listed.get(name)
        if path is None:
            problems.append(f"{shown}: ありません（exporter は必ず生成する）")
            continue
        if entry is None:
            text = path.read_text(encoding="utf-8", errors="replace")
            problems.extend(f"{shown}: {hit}" for hit in denylist_hits(text) + scrub_hits(text, patterns))
            continue
        text = _read_exported(path, shown, entry["sha256"], problems)
        if text is None:
            continue
        problems.extend(f"{shown}: {hit}" for hit in scrub_hits(text, patterns) + denylist_hits(text))

    for path_str, entry in listed.items():
        shown = f"{NOTES_DIR}/{path_str}"
        path = on_disk.get(path_str)
        if path is None:
            problems.append(f"{shown}: manifest に載っているのに存在しません")
            continue
        text = _read_exported(path, shown, entry["sha256"], problems)
        if text is None:
            continue

        try:
            fields = parse_frontmatter(text)
        except ValueError as error:
            problems.append(f"{shown}: {error}")
            fields = None
        if fields is not None:
            if fields.get("scope") != "public":
                problems.append(f"{shown}: `scope: public` ではありません: {fields.get('scope')!r}")
            source = fields.get("source")
            if not isinstance(source, str) or not source.startswith(SOURCE_PREFIX):
                problems.append(f"{shown}: `source:` が {SOURCE_PREFIX!r} で始まっていません: {source!r}")
            if fields.get("id") != entry["id"]:
                problems.append(f"{shown}: frontmatter の id {fields.get('id')!r} が manifest の {entry['id']!r} と違います")
            if fields.get("type") == "digest":
                problems.append(f"{shown}: `type: digest` は公開できません")

        problems.extend(f"{shown}: {hit}" for hit in scrub_hits(text, patterns) + denylist_hits(text))
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else Path(__file__).resolve().parents[1]
    if args and not root.is_dir():
        print(f"パスが存在しません: {root}", file=sys.stderr)
        return 2
    notes_dir = root / NOTES_DIR
    if not notes_dir.exists() and not notes_dir.is_symlink():
        print(f"OK: {NOTES_DIR}/ はまだありません（検査対象なし）")
        return 0
    problems = check(root)
    if problems:
        print(f"{NOTES_DIR}/ の問題 {len(problems)} 件（このディレクトリは手編集禁止。非公開 KB 側で直して再 export）:")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"OK: {NOTES_DIR}/ は exporter の manifest と一致し、manifest 含め禁止語もありません")
    return 0


if __name__ == "__main__":
    sys.exit(main())
