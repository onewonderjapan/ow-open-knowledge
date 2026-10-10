#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/check_kb_export.py の回帰。knowledge-notes/ は exporter の出力以外を受け付けない。"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
# ローカル禁止語のダミー（実際の組織固有の語はリポジトリに置かない）
LOCAL_TERMS = ("~/example-outbox", "example-internal-dir/")
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

    def __init__(self, root: Path, dirname: str = "knowledge-notes"):
        self.root = root
        self.dir = root / dirname
        self.dir.mkdir()
        self.notes: list[dict] = []
        # 3 本目はローカル禁止語（ダミー）と同じ文字列。manifest 検査で scrub_patterns の値が除外される証拠になる。
        self.scrub_patterns = [r"社内コード名\w+", r"(?i)secret-project", r"example-internal-dir/"]
        (self.dir / "README.md").write_text("# knowledge-notes\n\n生成物。手編集しない。\n", encoding="utf-8")
        (self.dir / "INDEX.md").write_text("# INDEX\n\n- exp-001\n- exp-002\n", encoding="utf-8")
        (self.dir / "LICENSE").write_text("MIT License\n\nCopyright (c) 2026 Example\n", encoding="utf-8")

    def sha(self, name: str) -> str:
        return hashlib.sha256((self.dir / name).read_bytes()).hexdigest()

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
            "generator": "kb export-public",
            "source_repo": "onewonderjapan/knowledge-base",
            "source_commit": "abc1234def",
            "exported_at": "2026-09-25",
            "count": len(self.notes),
            "scrub_patterns": self.scrub_patterns,
            "notes": self.notes,
            "files": [{"path": n, "sha256": self.sha(n)} for n in ("README.md", "INDEX.md", "LICENSE")],
        }
        manifest.update(overrides)
        (self.dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


class CheckKbExportTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module(MODULE_PATH, "check_kb_export")
        # 組織固有の禁止語はローカルからしか来ない。テストではダミー値に固定する。
        self.module.DENYLIST = LOCAL_TERMS
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
        fx.add_note("exp-001", note_text("exp-001", body="ログは ~/example-outbox/run1 にある。\n"))
        fx.write_manifest()
        problems = self.assertProblem("ローカル禁止語に一致")
        self.assertFalse(any("example-outbox" in p for p in problems), problems)  # 語そのものは出さない
        self.assertTrue(any("11 行目" in p for p in problems), problems)

    def test_denylist_windows_path_in_frontmatter(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", note_type="experiment\norigin: C:\\video-plan"))
        fx.write_manifest()
        self.assertProblem("禁止パターン（Windows ドライブパス）")

    def test_denylist_hit_in_index_files(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "INDEX.md").write_text("# INDEX\n\nhost = 192.168.0.10\n", encoding="utf-8")
        self.assertProblem("INDEX.md: 3 行目: 禁止パターン（RFC1918 プライベート IP）")

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

    # --- manifest.json 自体の内容検査 ---

    def test_manifest_denylist_in_source_commit(self):
        self.happy().write_manifest(source_commit="/home/someuser/kb@abc")
        self.assertProblem("manifest.json: $.source_commit: 禁止パターン（/home/<user> パス）")

    def test_manifest_denylist_in_note_id(self):
        fx = Fixture(self.root)
        fx.add_note("example-internal-dir/leak", note_text("example-internal-dir/leak"), path="leak.md")
        fx.write_manifest()
        self.assertProblem("manifest.json: $.notes[0].id: ローカル禁止語に一致")

    def test_manifest_denylist_in_extra_field(self):
        self.happy().write_manifest(debug_host="10.1.2.3")
        self.assertProblem("manifest.json: $.debug_host: 禁止パターン（RFC1918 プライベート IP）")

    def test_manifest_denylist_in_extra_key(self):
        self.happy().write_manifest(**{"~/example-outbox": "x"})
        self.assertProblem("manifest.json: $ のキー: ローカル禁止語に一致")

    def test_manifest_scrub_pattern_hit(self):
        self.happy().write_manifest(note="Secret-Project 由来")
        self.assertProblem("manifest.json: $.note: scrub_pattern")

    def test_manifest_scrub_patterns_value_is_not_scanned(self):
        """scrub_patterns 自体は検出語を含むのが正常。自分自身に当たって落ちてはいけない。"""
        fx = self.happy()
        fx.write_manifest()
        self.assertIn("example-internal-dir/", fx.scrub_patterns)
        self.assertEqual(self.module.check(self.root), [])

    # --- 汎用パターンとローカル禁止語の読み込み ---

    def test_generic_token_patterns(self):
        for n, body in enumerate(("key AKIA" + "A" * 16, "tok ghp_" + "a" * 30, "-----BEGIN RSA PRIVATE KEY-----")):
            with self.subTest(body=body):
                sub = self.root / f"case{n}"
                sub.mkdir()
                fx = Fixture(sub)
                fx.add_note("exp-001", note_text("exp-001", body=body + "\n"))
                fx.write_manifest()
                problems = self.module.check(fx.root)
                self.assertTrue(any("禁止パターン" in p for p in problems), problems)

    def test_public_ip_is_not_flagged(self):
        fx = Fixture(self.root)
        fx.add_note("exp-001", note_text("exp-001", body="公開 DNS 8.8.8.8 と 172.32.0.1 は対象外。\n"))
        fx.write_manifest()
        self.assertEqual(self.module.check(self.root), [])

    def test_load_local_denylist_from_env_and_file(self):
        local = self.root / "deny.local.txt"
        local.write_text("# コメント\nexample-host-a  # 行末コメント\n\nexample-dir/\n", encoding="utf-8")
        old = {k: os.environ.get(k) for k in ("KB_EXPORT_DENYLIST", "KB_EXPORT_DENYLIST_FILE")}
        try:
            os.environ["KB_EXPORT_DENYLIST"] = "example-env-term\nexample-dir/"
            os.environ["KB_EXPORT_DENYLIST_FILE"] = str(local)
            terms = self.module.load_local_denylist()
        finally:
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        self.assertEqual(terms, ("example-env-term", "example-dir/", "example-host-a"))

    def test_no_local_denylist_means_generic_only(self):
        old = {k: os.environ.pop(k, None) for k in ("KB_EXPORT_DENYLIST", "KB_EXPORT_DENYLIST_FILE")}
        try:
            self.module.LOCAL_DENYLIST_DEFAULT = self.root / "missing.local.txt"
            self.assertEqual(self.module.load_local_denylist(), ())
        finally:
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v

    def test_example_file_has_no_real_terms_and_local_file_is_ignored(self):
        example = (REPO_ROOT / "scripts" / "kb_export_denylist.example.txt").read_text(encoding="utf-8")
        self.assertIn("example", example)
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("scripts/kb_export_denylist.local.txt", gitignore)

    # --- 重複キーと生テキスト検査 ---

    def write_raw_manifest(self, fx: Fixture, mutate) -> None:
        """正規の manifest を書いてから生テキストを mutate で書き換える（json.dumps では作れない形用）。"""
        fx.write_manifest()
        path = fx.dir / "manifest.json"
        path.write_text(mutate(path.read_text(encoding="utf-8")), encoding="utf-8")

    def test_duplicate_top_level_key_fails(self):
        fx = self.happy()
        self.write_raw_manifest(
            fx, lambda raw: raw.replace('"source_commit": ', '"source_commit": "/home/someuser",\n  "source_commit": ', 1)
        )
        problems = self.assertProblem("キー 'source_commit' が重複しています")
        # 後勝ちで捨てられる値も、生テキスト検査で拾われる
        self.assertTrue(any("生テキスト" in p and "/home/<user>" in p for p in problems), problems)

    def test_duplicate_nested_key_fails(self):
        fx = self.happy()
        self.write_raw_manifest(fx, lambda raw: raw.replace('"id": "exp-001"', '"id": "x", "id": "exp-001"', 1))
        self.assertProblem("キー 'id' が重複しています")
        self.assertEqual(self.run_main(), 1)

    def test_duplicate_key_without_denylist_value_still_fails(self):
        fx = self.happy()
        self.write_raw_manifest(
            fx, lambda raw: raw.replace('"exported_at": ', '"exported_at": "2026-01-01",\n  "exported_at": ', 1)
        )
        self.assertProblem("キー 'exported_at' が重複しています")

    def test_raw_text_denylist_outside_scrub_patterns(self):
        fx = self.happy()
        # JSON エスケープ（\\）越しの Windows パスも生テキストで当たる
        fx.write_manifest(origin="C:\\video-plan")
        problems = self.assertProblem("生テキスト")
        self.assertTrue(any("Windows ドライブパス" in p for p in problems), problems)

    def test_raw_text_denylist_in_json_whitespace_region(self):
        """値の外（パースで消える部分）に置かれた禁止語も拾う。"""
        fx = self.happy()
        self.write_raw_manifest(fx, lambda raw: raw.replace("{", "{\"192.168.1.1\": 1,", 1))
        self.assertProblem("生テキスト")

    def test_scrub_patterns_with_denylist_text_pass_raw_scan(self):
        fx = self.happy()
        fx.scrub_patterns = [
            r"/home/someuser\S*",
            r"192\.168\.0\.10",
            "C:\\\\",  # 正規表現としての C:\\
            "~/example-outbox",
            r"example-internal-dir/[\w-]+",
            r"(?i)example-internal-dir/ \[\]{}:,",  # 括弧・カンマを含んでもトークン単位で塗れる
        ]
        fx.write_manifest()
        self.assertEqual(self.module.check(self.root), [])

    def test_scrub_patterns_escaped_slash_is_still_masked(self):
        """exporter が `/` を `\\/` とエスケープして書いても、塗りつぶしはトークン単位なので通る。"""
        fx = self.happy()
        fx.scrub_patterns = ["~/example-outbox", "example-internal-dir/", "other/"]
        self.write_raw_manifest(fx, lambda raw: raw.replace('"~/example-outbox"', '"~\\/example-outbox"'))
        self.assertIn("~\\/example-outbox", (fx.dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(self.module.check(self.root), [])

    def test_nested_scrub_patterns_key_is_not_masked(self):
        """トップレベル以外の `scrub_patterns` は塗らない（隠れ蓑にさせない）。"""
        fx = self.happy()
        fx.write_manifest(extra={"scrub_patterns": ["/home/someuser"]})
        self.assertProblem("生テキスト")

    # --- scrub_patterns の件数 ---

    def test_empty_scrub_patterns_fails(self):
        fx = self.happy()
        fx.scrub_patterns = []
        fx.write_manifest()
        self.assertProblem("scrub_patterns は 3 件以上")

    def test_too_few_scrub_patterns_fails(self):
        fx = self.happy()
        fx.scrub_patterns = ["a", "b"]
        fx.write_manifest()
        self.assertProblem("scrub_patterns は 3 件以上")

    # --- README.md / INDEX.md（manifest.files）---

    def test_files_field_missing(self):
        fx = self.happy()
        fx.write_manifest()
        manifest_path = fx.dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        del manifest["files"]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        self.assertProblem("files が配列ではありません")

    def test_files_must_list_exactly_readme_and_index(self):
        fx = self.happy()
        fx.write_manifest(files=[{"path": "README.md", "sha256": fx.sha("README.md")}])
        self.assertProblem("files はちょうど")

    def test_license_must_be_mit(self):
        fx = self.happy()
        (fx.dir / "LICENSE").write_text("Proprietary\n", encoding="utf-8")
        fx.write_manifest()
        self.assertProblem("LICENSE: MIT License ではありません")

    def test_license_missing(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "LICENSE").unlink()
        self.assertProblem("LICENSE: ありません")

    def test_readme_sha_mismatch(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "README.md").write_text("# knowledge-notes\n\n手で書き換えた。\n", encoding="utf-8")
        self.assertProblem("README.md: sha256 が manifest と一致しません")

    def test_index_sha_mismatch(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "INDEX.md").write_text("# INDEX\n\n- exp-001\n", encoding="utf-8")
        self.assertProblem("INDEX.md: sha256 が manifest と一致しません")

    def test_index_scrub_pattern_hit(self):
        fx = self.happy()
        (fx.dir / "INDEX.md").write_text("# INDEX\n\n- 社内コード名ALPHA\n", encoding="utf-8")
        fx.write_manifest()  # sha は一致させ、scrub だけで落ちることを確かめる
        problems = self.assertProblem("INDEX.md: 3 行目: scrub_pattern")
        self.assertFalse(any("sha256" in p for p in problems), problems)

    def test_readme_scrub_pattern_hit(self):
        fx = self.happy()
        (fx.dir / "README.md").write_text("# notes\n\nsecret-project の記録\n", encoding="utf-8")
        fx.write_manifest()
        self.assertProblem("README.md: 3 行目: scrub_pattern")

    def test_readme_missing(self):
        fx = self.happy()
        fx.write_manifest()
        (fx.dir / "README.md").unlink()
        self.assertProblem("README.md: ありません")

    def test_readme_invalid_utf8_fails_closed(self):
        fx = self.happy()
        (fx.dir / "README.md").write_bytes(b"# notes\n\xff\xfe broken\n")
        fx.write_manifest()
        self.assertProblem("README.md: UTF-8 として読めません")

    # --- シンボリックリンク ---

    def test_symlinked_notes_dir_fails(self):
        real = Fixture(self.root, dirname="real-notes")
        real.add_note("exp-001")
        real.write_manifest()
        link = self.root / "knowledge-notes"
        try:
            link.symlink_to(real.dir, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"symlink を作れない環境: {error}")
        self.assertProblem("ディレクトリ自体がシンボリックリンク")
        self.assertEqual(self.run_main(), 1)

    def test_dangling_symlinked_notes_dir_fails(self):
        link = self.root / "knowledge-notes"
        try:
            link.symlink_to(self.root / "nowhere", target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"symlink を作れない環境: {error}")
        self.assertEqual(self.run_main(), 1)

    def test_explicit_missing_root_fails(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.module.main([str(self.root / "no-such-dir")]), 2)


if __name__ == "__main__":
    unittest.main()
