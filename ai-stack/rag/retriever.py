# -*- coding: utf-8 -*-
"""社内文書の類似検索（薄切片版: janome分かち書き + BM25）

本格版はベクトル検索(multilingual-e5 + Qdrant)に差し替える。
インターフェース(search)は据え置きなので上位層は無変更で移行できる。
"""
import math
import re
from collections import Counter
from pathlib import Path

from janome.tokenizer import Tokenizer

_tok = Tokenizer()
_STOP = set("の に は を た が で て と し れ さ ある いる する です ます から など まで これ それ".split())


def tokenize(text: str) -> list[str]:
    words = []
    for t in _tok.tokenize(text):
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

    def add_dir(self, root: str, glob: str = "**/*.md"):
        for p in sorted(Path(root).glob(glob)):
            text = p.read_text(encoding="utf-8")
            toks = tokenize(text)
            self.docs.append({"id": len(self.docs), "path": str(p), "title": p.stem, "text": text, "tokens": toks})
        for d in self.docs:
            for w in set(d["tokens"]):
                self.df[w] += 1
        self.avgdl = sum(len(d["tokens"]) for d in self.docs) / max(1, len(self.docs))

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
