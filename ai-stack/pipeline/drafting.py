# -*- coding: utf-8 -*-
"""起草プロンプトの組立（CLI `pipeline/run.py` と Web UI `ui/app.py` の共有部分）

ここに集約する理由:
  1. 章立ては evalkit.REQUIRED_SECTIONS を単一の真実源として生成する。
     プロンプト側とQC側に別々に書くと必ず漏れる（実際に外部連携/移行・運用が漏れていた）。
  2. **出境するテキストは全てここを通す**。要件書だけ脱敏して先例文書を生テキストで
     送っていた事故を構造的に防ぐ。→ PITFALLS.md 19
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evalkit.structure_check import REQUIRED_SECTIONS   # noqa: E402

# 先例1件あたりプロンプトに載せる最大文字数
REF_MAX_CHARS = 2500

_CHAPTERS = " / ".join(f"{i}. {s}" for i, s in enumerate(REQUIRED_SECTIONS, 1))

PROMPT_TEMPLATE = f"""あなたはSIerの上級システムエンジニア。以下の顧客要件から「基本設計書のドラフト」を日本語で作成せよ。

# 社内標準の章立て(必須・この順)
{_CHAPTERS}

# 過去の類似プロジェクトの設計書(参考。書式・粒度を踏襲すること)
{{references}}

# 顧客要件(機密は伏せ字済み。伏せ字はそのまま使うこと)
{{requirements}}

Markdownで、各章に具体的な内容を記述。推測が必要な箇所は「【要確認】」を付けて仮置きする。"""


def build_references(hits: list[dict], masker, mapping: dict | None = None) -> tuple[str, dict]:
    """召回した先例文書を脱敏してプロンプト用テキストに組み立てる。

    戻り値: (プロンプトに差し込むテキスト, 更新後の mapping)

    注意:
      - 脱敏してから切り詰める。逆順にすると境界で実体が分断され、断片が漏れる。
      - タイトルも脱敏する。ファイル名(`design_田中商事.md` 等)に顧客名が入りうる。
      - 要件書の mapping を渡して採番を共有する。文書ごとに採番を振り直すと
        別会社が同じラベルになり監査表が壊れる。
    """
    mapping = {} if mapping is None else mapping
    if not hits:
        return "(先例なし)", mapping
    parts: list[str] = []
    for h in hits:
        masked_text, _ = masker.mask(h["text"], mapping)
        masked_title, _ = masker.mask(h["title"], mapping)
        parts.append(f"【{masked_title}】\n{masked_text[:REF_MAX_CHARS]}")
    return "\n\n---\n\n".join(parts), mapping


def build_prompt(masked_requirements: str, references_text: str) -> str:
    return PROMPT_TEMPLATE.format(references=references_text, requirements=masked_requirements)
