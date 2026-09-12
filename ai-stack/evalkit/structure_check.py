# -*- coding: utf-8 -*-
"""設計書ドラフトの構造検査（ローカル質検層の薄切片）

決定論的チェック: 必須章の欠落 / 空章 / マスク漏れの疑い。
LLM評価(rubric採点)は evalkit/judge.py として今後追加。

REQUIRED_SECTIONS はプロンプト側(pipeline/drafting.py)からも参照される単一の真実源。
検査項目を増やすときはここだけを直す。
マスク漏れ検知は masking 層と同じ正規表現を使う。**検査者が生成者より緩いと検査の意味がない**
（agent-cultivation/AGENT育成標準.md「生成者と検査者は分離する」の実装）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from masking.masker import LEAK_PATTERNS, normalize   # noqa: E402

REQUIRED_SECTIONS = [
    "概要", "システム構成", "機能一覧", "画面設計",
    "データ設計", "外部連携", "非機能要件", "移行・運用",
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
    # マスク漏れ検知は正規化後に行う（全角のまま書かれた電話番号を見逃さない）
    normalized = normalize(draft)
    for tag, pat in LEAK_PATTERNS:
        m = pat.search(normalized)
        if m:
            findings.append(f"マスク漏れの疑い({tag}): {m.group(0)}")
    for name in known_real_names or []:
        if normalize(name) in normalized:
            findings.append(f"実名の混入: {name}")
    return {"ok": not findings, "findings": findings, "sections_found": headers}
