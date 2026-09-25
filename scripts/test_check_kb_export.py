#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/check_kb_export.py の回帰。knowledge-notes/ は exporter の出力以外を受け付けない。"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = Path(__file__).resolve().parent / "check_kb_export.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def note_text(note_id: str, *, scope="public", source="knowledge-base@abc1234", note_type="experiment",
              body="事前登録した実験の結果。\n") -> str:
    lines = ["---", f"id: {note_id}"]
    if scope is not None:
        lines.append(f"scope: {scope}")
    if source is not None:
        lines.append(f"source: {source}")
    if note_type is not None:
        lines.append(f"type: {note_type}")
    lines += ["tags: [ai, eval]", "---", "", f"# {note_id}", "", body]
    return "\n".join(lines)


class Fixture:
    """tmp 内に exporter 出力相当の knowledge-notes/ を組み立てる。"""

    def __init__(self, root: Path):
        self.root = root
        self.dir = root / "knowledge-notes"
        self.dir.mkdir()
        self.notes: list[dict] = []
        self.scrub_patterns = [r"社内コード名\w+", r"(?i)secret-project"]

    def add_note(self, note_id: str, text: str | None = None, path: str | None = None) -> Path:
        rel = path or f"{note_id}.md"
        target = self.dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text if text is not None else note_text(note_id), encoding="utf-8")
        self.notes.append(
            {"id": note_id, "path": rel, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
        )
        return target

    def write_manifest(self, **overrides) -> None:
        manifest = {
            "generator": "scripts/kb.py export-public",
            "source_repo": "onewonderjapan/knowledge-base",
            "source_commit": "abc1234def",
            "exported_at": "2026-09-25",
            "count": len(self.notes),
            "scrub_patterns": self.scrub_patterns,
            "notes": self.notes,
        }
        manifest.update(overrides)
        (self.dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


class CheckKbExportTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(MODULE_PATH, "check_kb_export")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def assertProblem(self, needle: str) -> list[str]:
        problems = self.module.check(self.root)
        self.assertTrue(any(needle in p for p in problems), problems)
        return problems

    def run_main(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return self.module.main([str(self.root)])

    def happy(self) -> Fixture:
        fx = Fixture(self.root)
        fx.add_note("exp-001")
        fx.add_note("exp-002", path="2026/exp-002.md")
        (fx.dir / "README.md").write_text("# knowledge-notes\n\n生成物。手編集しない。\n", encoding="utf-8")
        (fx.dir / "INDEX.md").write_text("# INDEX\n\n- exp-001\n- exp-002\n", encoding="utf-8")
        return fx

    def test_repo_state_passes(self):
        self.assertEqual(self.module.check(REPO_ROOT), [])

    def test_missing_directory_exits_zero(self):
        self.assertEqual(self.module.check(self.root), [])
        self.assertEqual(self.run_main(), 0)

    def test_happy_path(self):
        self.happy().write_manifest()
        self.assertEqual(self.module.check(self.root), [])
        self.assertEqual(self.run_main(), 0)

    def test_missing_manifest(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001")
        self.assertProblem("manifest.json: ありません")
        self.assertEqual(self.run_main(), 1)

    def test_bad_generator_and_date(self):
        fx = self.happy()
        fx.write_manifest(generator="hand", exported_at="2026/09/25")
        self.assertProblem("generator")
        self.assertProblem("exported_at")

    def test_count_mismatch(self):
        fx = self.happy()
        fx.write_manifest(count=5)
        self.assertProblem("count=5")

    def test_sha_mismatch(self):
        fx = self.happy()
        fx.write_manifest()
        path = fx.dir / "exp-001.md"
        path.write_text(path.read_text(encoding="utf-8") + "手で追記。\n", encoding="utf-8")
        self.assertProblem("sha256 が manifest と一致しません")
        self.assertEqual(self.run_main(), 1)

    def test_unlisted_file(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "hand-written.md").write_text(note_text("hand-written"), encoding="utf-8")
        self.assertProblem("hand-written.md: manifest に載っていません")

    def test_listed_but_missing(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "exp-001.md").unlink()
        self.assertProblem("存在しません")

    def test_extra_non_markdown_file(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "notes.txt").write_text("x\n", encoding="utf-8")
        self.assertProblem("非 Markdown")

    def test_bad_scope(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", scope="internal"))
        fx.write_manifest()
        self.assertProblem("scope: public")

    def test_missing_source(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", source=None))
        fx.write_manifest()
        self.assertProblem("source:")

    def test_wrong_source_prefix(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", source="elsewhere@abc"))
        fx.write_manifest()
        self.assertProblem("source:")

    def test_digest_type(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", note_type="digest"))
        fx.write_manifest()
        self.assertProblem("type: digest")

    def test_id_mismatch(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-999"))
        fx.write_manifest()
        self.assertProblem("id 'exp-999'")

    def test_missing_frontmatter(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", "# exp-001\n\n本文だけ。\n")
        fx.write_manifest()
        self.assertProblem("frontmatter がありません")

    def test_block_list_frontmatter_is_accepted(self):
        fx = Fixture(self.root)
        text = note_text("exp-001").replace("tags: [ai, eval]", "tags:\n  - ai\n  - eval")
        fx.add_note("exp-001", text)
        fx.write_manifest()
        self.assertEqual(self.module.check(self.root), [])

    def test_denylist_hit_in_note(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", body="ログは ~/outbox/run1 にある。\n"))
        fx.write_manifest()
        problems = self.assertProblem("禁止語 '~/outbox'")
        self.assertTrue(any("11 行目" in p for p in problems), problems)

    def test_denylist_windows_path_in_frontmatter(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", note_type="experiment\norigin: C:\\video-plan"))
        fx.write_manifest()
        self.assertProblem("禁止語 'C:\\\\'")

    def test_denylist_hit_in_index_files(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "INDEX.md").write_text("# INDEX\n\nS1 = 172.72.0.1\n", encoding="utf-8")
        self.assertProblem("INDEX.md: 3 行目: 禁止語 '172.72.'")

    def test_scrub_pattern_hit(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", body="Secret-Project の件で検証した。\n"))
        fx.write_manifest()
        self.assertProblem("scrub_pattern")

    def test_invalid_scrub_pattern(self):
        fx = self.happy()
        fx.scrub_patterns = ["(unclosed"]
        fx.write_manifest()
        self.assertProblem("正規表現として不正")

    def test_path_traversal_in_manifest(self):
        fx = self.happy()
        fx.notes.append({"id": "evil", "path": "../README.md", "sha256": "0" * 64})
        fx.write_manifest()
        self.assertProblem("不正なパス")

    def test_explicit_missing_root_fails(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.module.main([str(self.root / "no-such-dir")]), 2)


if __name__ == "__main__":
    unittest.main()
