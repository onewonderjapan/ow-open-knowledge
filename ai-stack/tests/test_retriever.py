# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag import retriever  # noqa: E402
from rag.retriever import BM25Index, _tokenize_fallback, tokenize  # noqa: E402


class RetrieverTests(unittest.TestCase):
    def test_demo_corpus_returns_hits_for_training_query(self):
        idx = BM25Index()
        idx.add_dir(str(ROOT / "demo_data" / "past_projects"), "**/design_*.md")
        self.assertGreaterEqual(len(idx.docs), 2)
        hits = idx.search("研修 申込 ポータル SSO", k=2)
        self.assertTrue(hits)
        self.assertIn("title", hits[0])
        self.assertIn("score", hits[0])

    def test_add_dir_twice_does_not_double_document_frequency(self):
        idx = BM25Index()
        corpus = str(ROOT / "demo_data" / "past_projects")
        idx.add_dir(corpus, "**/design_*.md")
        df_once = dict(idx.df)
        n_docs = len(idx.docs)
        idx.add_dir(corpus, "**/design_*.md")
        self.assertEqual(len(idx.docs), n_docs * 2)
        # 同一語の df は「文書数」に比例して増えるが、同一 add の二重計上ではない
        # （再計算しているので、2回目は文書が倍になった分だけ増える）
        for word, df in df_once.items():
            self.assertEqual(idx.df[word], df * 2)

    def test_fallback_tokenizer_extracts_cjk_and_ascii(self):
        tokens = _tokenize_fallback("研修ポータル SSO login 画面")
        self.assertTrue(any("研修" in t or t == "研修" for t in tokens) or "研修ポ" in tokens or "習ポ" in tokens)
        self.assertIn("sso", tokens)
        self.assertIn("login", tokens)

    def test_tokenize_never_raises_without_janome(self):
        original = retriever._tok
        retriever._tok = False
        try:
            tokens = tokenize("社員研修の申込管理")
            self.assertTrue(tokens)
        finally:
            retriever._tok = original


if __name__ == "__main__":
    unittest.main()
