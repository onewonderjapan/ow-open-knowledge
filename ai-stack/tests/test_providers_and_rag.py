# -*- coding: utf-8 -*-
"""プロバイダ登録と RAG インデックスの回帰テスト

janome が入っていない環境では RAG 側のテストはスキップする。
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from llm.providers import (BaseProvider, available_providers, get_provider,   # noqa: E402
                           register_provider)

try:
    from rag.retriever import BM25Index
    HAS_JANOME = True
except ImportError:      # janome 未導入
    HAS_JANOME = False


class TestProviderRegistry(unittest.TestCase):
    def test_builtin_providers(self):
        self.assertEqual(available_providers(), ["anthropic-api", "claude-cli", "stub"])

    def test_stub_roundtrip(self):
        p = get_provider("stub")
        self.assertEqual(p.name, "stub")
        self.assertIn("概要", p.complete("なにか"))

    def test_unknown_provider_lists_options(self):
        with self.assertRaises(ValueError) as cm:
            get_provider("gpt-9")
        self.assertIn("stub", str(cm.exception))

    def test_register_new_provider_without_touching_core(self):
        class EchoProvider(BaseProvider):
            name = "echo"

            def complete(self, prompt: str) -> str:
                return prompt

        register_provider("echo", EchoProvider)
        try:
            self.assertEqual(get_provider("echo").complete("やまびこ"), "やまびこ")
        finally:
            from llm import providers
            providers._REGISTRY.pop("echo", None)

    def test_kwargs_forwarded(self):
        p = get_provider("claude-cli", model="test-model")
        self.assertEqual(p.model, "test-model")


@unittest.skipUnless(HAS_JANOME, "janome 未導入")
class TestBM25AddDir(unittest.TestCase):
    def _corpus(self, **files) -> str:
        d = Path(tempfile.mkdtemp())
        for name, body in files.items():
            (d / name).write_text(body, encoding="utf-8")
        return str(d)

    def test_add_dir_twice_matches_single_call(self):
        """全docsを毎回数え直す実装では2回目で既存文書のdfが二重計上されIDFが壊れる。

        2ディレクトリを2回に分けて読んだ場合と、同じ2文書を1回で読んだ場合の df が一致すること。
        """
        doc_a, doc_b = "在庫管理システムの設計", "予約ポータルの設計"
        split_1 = self._corpus(**{"a.md": doc_a})
        split_2 = self._corpus(**{"b.md": doc_b})
        combined = self._corpus(**{"a.md": doc_a, "b.md": doc_b})

        two_calls = BM25Index()
        two_calls.add_dir(split_1)
        two_calls.add_dir(split_2)

        one_call = BM25Index()
        one_call.add_dir(combined)

        self.assertEqual(len(two_calls.docs), len(one_call.docs))
        self.assertEqual(two_calls.df, one_call.df)
        self.assertAlmostEqual(two_calls.avgdl, one_call.avgdl)

    def test_df_never_exceeds_doc_count(self):
        a = self._corpus(**{"a.md": "設計書", "b.md": "設計書"})
        idx = BM25Index()
        idx.add_dir(a)
        idx.add_dir(a)   # 意図的に同じディレクトリを2回
        for word, count in idx.df.items():
            self.assertLessEqual(count, len(idx.docs), f"df が文書数を超えた: {word}={count}")

    def test_search_returns_hits(self):
        d = self._corpus(**{"design_a.md": "在庫管理システムをWebへ移行する設計書"})
        idx = BM25Index()
        idx.add_dir(d, "**/design_*.md")
        hits = idx.search("在庫管理の設計", k=1)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["title"], "design_a")


if __name__ == "__main__":
    unittest.main(verbosity=2)
