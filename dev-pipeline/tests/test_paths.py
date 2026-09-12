# -*- coding: utf-8 -*-
"""workspace 境界の回帰テスト

Agent が扱うパスは LLM 出力由来 = 信頼できない入力。
`workspace / "../../etc/passwd"` が通ると任意ファイル書き込み・削除になる。

実行: python3 -m unittest discover -s dev-pipeline/tests -t dev-pipeline
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.paths import PathEscapeError, resolve_in_workspace   # noqa: E402


class TestResolveInWorkspace(unittest.TestCase):
    def setUp(self):
        self.ws = Path(tempfile.mkdtemp()) / "workspace"
        self.ws.mkdir()

    def test_plain_relative_path(self):
        got = resolve_in_workspace(self.ws, "app.py")
        self.assertEqual(got, (self.ws / "app.py").resolve())

    def test_nested_relative_path(self):
        got = resolve_in_workspace(self.ws, "src/pkg/mod.py")
        self.assertEqual(got, (self.ws / "src/pkg/mod.py").resolve())

    def test_inner_dotdot_still_inside_is_allowed(self):
        got = resolve_in_workspace(self.ws, "src/../app.py")
        self.assertEqual(got, (self.ws / "app.py").resolve())

    def test_parent_escape_rejected(self):
        for bad in ("../secrets.txt", "../../etc/passwd", "a/../../b", "./../x"):
            with self.assertRaises(PathEscapeError, msg=f"許可された: {bad}"):
                resolve_in_workspace(self.ws, bad)

    def test_absolute_path_rejected(self):
        # Path("ws") / "/etc/passwd" は "/etc/passwd" になる（右辺が絶対だと左辺が捨てられる）
        with self.assertRaises(PathEscapeError):
            resolve_in_workspace(self.ws, "/etc/passwd")

    def test_empty_path_rejected(self):
        for bad in ("", "   "):
            with self.assertRaises(PathEscapeError):
                resolve_in_workspace(self.ws, bad)

    def test_symlink_escape_rejected(self):
        outside = self.ws.parent / "outside"
        outside.mkdir()
        link = self.ws / "link"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("シンボリックリンクを作れない環境")
        with self.assertRaises(PathEscapeError):
            resolve_in_workspace(self.ws, "link/stolen.txt")

    def test_sibling_prefix_not_confused(self):
        # "workspace-evil" は "workspace" の接頭辞を共有するが配下ではない
        evil = self.ws.parent / f"{self.ws.name}-evil"
        evil.mkdir()
        with self.assertRaises(PathEscapeError):
            resolve_in_workspace(self.ws, f"../{evil.name}/x.txt")


if __name__ == "__main__":
    unittest.main(verbosity=2)
