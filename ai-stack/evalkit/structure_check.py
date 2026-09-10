# -*- coding: utf-8 -*-
"""設計書ドラフトの構造検査（ローカル質検層の薄切片）

決定論的チェック: 必須章の欠落 / 空章 / マスク漏れの疑い。
LLM評価(rubric採点)は evalkit/judge.py として今後追加。
"""
import re

REQUIRED_SECTIONS = ["概要", "システム構成", "機能一覧", "画面設計", "データ設計", "非機能要件"]

# マスク漏れ検知: 生の電話/メール/実在っぽい社名が残っていないか
_LEAK_PATTERNS = [
    ("PHONE", re.compile(r"0\d{1,4}-\d{1,4}-\d{3,4}")),
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
]


def check(draft: str, known_real_names: list[str] | None = None) -> dict:
    findings = []
    headers = re.findall(r"^#+\s*(?:\d+[.．]?\s*)?(.+)$", draft, re.M)
    header_text = " ".join(headers)
    for sec in REQUIRED_SECTIONS:
        if sec not in header_text and sec not in draft:
            findings.append(f"必須章が見当たらない: {sec}")
    # 空章（見出しの直後に次の見出し）。文書タイトル(h1)は対象外
    for m in re.finditer(r"^(##+\s*.+)\n+(?=#+\s)", draft, re.M):
        findings.append(f"空の章: {m.group(1).strip()}")
    for tag, pat in _LEAK_PATTERNS:
        if pat.search(draft):
            findings.append(f"マスク漏れの疑い({tag}): {pat.search(draft).group(0)}")
    for name in known_real_names or []:
        if name in draft:
            findings.append(f"実名の混入: {name}")
    return {"ok": not findings, "findings": findings, "sections_found": headers}
