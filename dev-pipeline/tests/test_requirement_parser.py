# -*- coding: utf-8 -*-
"""要件ファイルパーサーの回帰テスト

実行: python3 -m unittest discover -s dev-pipeline/tests -t dev-pipeline/tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.requirement_parser import parse_requirement_file   # noqa: E402


def write(text: str) -> Path:
    p = Path(tempfile.mkdtemp()) / "req.md"
    p.write_text(text, encoding="utf-8")
    return p


class TestHeaderParsing(unittest.TestCase):
    def test_standard_form(self):
        spec = parse_requirement_file(write(
            "branch: feature/login\n"
            "repo: https://github.com/u/p.git\n"
            "---\n"
            "ログイン機能を追加する\n"
        ))
        self.assertEqual(spec.branch, "feature/login")
        self.assertEqual(spec.repo, "https://github.com/u/p.git")
        self.assertEqual(spec.content, "ログイン機能を追加する")

    def test_header_optional(self):
        spec = parse_requirement_file(write("Azure と AWS を比較調査する\n"))
        self.assertIsNone(spec.branch)
        self.assertIsNone(spec.repo)
        self.assertEqual(spec.content, "Azure と AWS を比較調査する")

    def test_branch_only(self):
        spec = parse_requirement_file(write("branch: fix/typo\n---\n誤字を直す\n"))
        self.assertEqual(spec.branch, "fix/typo")
        self.assertIsNone(spec.repo)

    def test_yaml_frontmatter_form(self):
        spec = parse_requirement_file(write(
            "---\nbranch: feature/x\nrepo: https://e.com/r.git\n---\n本文です\n"
        ))
        self.assertEqual(spec.branch, "feature/x")
        self.assertEqual(spec.repo, "https://e.com/r.git")
        self.assertEqual(spec.content, "本文です")

    def test_case_insensitive_keys(self):
        spec = parse_requirement_file(write("Branch: feature/x\nREPO: https://e.com/r.git\n---\n本文\n"))
        self.assertEqual(spec.branch, "feature/x")
        self.assertEqual(spec.repo, "https://e.com/r.git")

    def test_url_colon_preserved(self):
        spec = parse_requirement_file(write("repo: https://github.com:443/u/p.git\n---\n本文\n"))
        self.assertEqual(spec.repo, "https://github.com:443/u/p.git")


class TestHeaderDoesNotLeakIntoBody(unittest.TestCase):
    """区切り線が無いと `branch:` 行が本文に残り、そのまま Agent に渡っていた。"""

    def test_no_separator(self):
        spec = parse_requirement_file(write(
            "branch: feature/login\nrepo: https://e.com/r.git\nログイン機能を追加する\n"
        ))
        self.assertEqual(spec.branch, "feature/login")
        self.assertNotIn("branch:", spec.content)
        self.assertNotIn("repo:", spec.content)
        self.assertEqual(spec.content, "ログイン機能を追加する")


class TestBodyIsNotTruncated(unittest.TestCase):
    """本文中の Markdown 水平線を区切り線と誤認し、手前の本文を捨てていた。"""

    def test_markdown_rule_in_body_without_header(self):
        body = "# 要件\n\n概要を書く\n\n---\n\n## 詳細\n詳細を書く"
        spec = parse_requirement_file(write(body))
        self.assertEqual(spec.content, body)
        self.assertIn("# 要件", spec.content)
        self.assertIn("## 詳細", spec.content)

    def test_markdown_rule_in_body_with_header(self):
        spec = parse_requirement_file(write(
            "branch: feature/x\n---\n# 要件\n概要\n\n---\n\n## 詳細\n詳細\n"
        ))
        self.assertEqual(spec.branch, "feature/x")
        self.assertIn("# 要件", spec.content)
        self.assertIn("## 詳細", spec.content)


class TestErrors(unittest.TestCase):
    def test_empty_body_raises(self):
        with self.assertRaises(ValueError):
            parse_requirement_file(write("branch: feature/x\n---\n\n"))

    def test_empty_file_raises(self):
        with self.assertRaises(ValueError):
            parse_requirement_file(write(""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
