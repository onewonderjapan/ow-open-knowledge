# -*- coding: utf-8 -*-
"""社内文書の類似検索（薄切片版: janome分かち書き + BM25）

本格版はベクトル検索(multilingual-e5 + Qdrant)に差し替える。
インターフェース(search)は据え置きなので上位層は無変更で移行できる。

janome が無い環境（ゼロ依存のデモ UI）では CJK バイグラム + ASCII 単語にフォールバックする。
"""
from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

_STOP = set("の に は を た が で て と し れ さ ある いる する です ます から など まで これ それ".split())
_tok = None  # janome Tokenizer | False (unavailable) | None (not tried)


def _janome_tokenizer():
    """Lazy-load janome so the demo UI can run with the standard library only."""
    global _tok
    if _tok is False:
        return None
    if _tok is None:
        try:
            from janome.tokenizer import Tokenizer
        except ImportError:
            _tok = False
            return None
        _tok = Tokenizer()
    return _tok


def _tokenize_fallback(text: str) -> list[str]:
    """janome 無しでも動く粗い分かち書き（CJK バイグラム + ASCII 単語）。"""
    words: list[str] = []
    for token in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{1,}", text.lower()):
        if token not in _STOP:
            words.append(token)
    for chunk in re.findall(r"[一-龥ァ-ヶぁ-ん]+", text):
        if len(chunk) == 1:
            if chunk not in _STOP:
                words.append(chunk)
        else:
            words.extend(chunk[i : i + 2] for i in range(len(chunk) - 1) if chunk[i : i + 2] not in _STOP)
    return words


def tokenize(text: str) -> list[str]:
    tokenizer = _janome_tokenizer()
    if tokenizer is None:
        return _tokenize_fallback(text)
    words = []
    for t in tokenizer.tokenize(text):
        base = t.base_form if t.base_form != "*" else t.surface
        pos = t.part_of_speech.split(",")[0]
        if pos in ("名詞", "動詞", "形容詞") and base not in _STOP and not re.fullmatch(r"[\s\d]+", base):
            words.append(base)
    return words


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs: list[dict] = []       # {id, path, title, text, tokens}
        self.df: Counter = Counter()
        self.avgdl = 0.0

    def _rebuild_stats(self) -> None:
        """add_dir を複数回呼んでも df が二重計上されないよう毎回再計算する。"""
        self.df = Counter()
        for d in self.docs:
            for w in set(d["tokens"]):
                self.df[w] += 1
        self.avgdl = sum(len(d["tokens"]) for d in self.docs) / max(1, len(self.docs))

    def add_dir(self, root: str, glob: str = "**/*.md"):
        for p in sorted(Path(root).glob(glob)):
            text = p.read_text(encoding="utf-8")
            toks = tokenize(text)
            self.docs.append({"id": len(self.docs), "path": str(p), "title": p.stem, "text": text, "tokens": toks})
        self._rebuild_stats()

    def search(self, query: str, k: int = 3) -> list[dict]:
        q = tokenize(query)
        n = len(self.docs)
        scored = []
        for d in self.docs:
            tf = Counter(d["tokens"])
            dl = len(d["tokens"])
            s = 0.0
            for w in q:
                if w not in tf:
                    continue
                idf = math.log(1 + (n - self.df[w] + 0.5) / (self.df[w] + 0.5))
                s += idf * tf[w] * (self.k1 + 1) / (tf[w] + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            if s > 0:
                scored.append((s, d))
        scored.sort(key=lambda x: -x[0])
        return [{"score": round(s, 2), "title": d["title"], "path": d["path"], "text": d["text"]} for s, d in scored[:k]]
