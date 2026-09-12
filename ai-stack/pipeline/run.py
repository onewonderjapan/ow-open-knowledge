# -*- coding: utf-8 -*-
"""端到端デモ: 要件書 → 脱敏 → 類似先例検索(RAG) → LLM起草 → 構造検査 → 出力

usage:
  python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
  python pipeline/run.py demo_data/incoming/new_rfp.md --provider claude-cli
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from masking.masker import Masker                    # noqa: E402
from rag.retriever import BM25Index                  # noqa: E402
from llm.providers import get_provider               # noqa: E402
from evalkit.structure_check import check            # noqa: E402

PROMPT_TEMPLATE = """あなたはSIerの上級システムエンジニア。以下の顧客要件から「基本設計書のドラフト」を日本語で作成せよ。

# 社内標準の章立て(必須・この順)
1. 概要 / 2. システム構成 / 3. 機能一覧 / 4. 画面設計 / 5. データ設計 / 6. 外部連携 / 7. 非機能要件 / 8. 移行・運用

# 過去の類似プロジェクトの設計書(参考。書式・粒度を踏襲すること)
{references}

# 顧客要件(機密は伏せ字済み。伏せ字はそのまま使うこと)
{requirements}

Markdownで、各章に具体的な内容を記述。推測が必要な箇所は「【要確認】」を付けて仮置きする。"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rfp", help="要件書ファイル(.md)")
    ap.add_argument("--provider", default="stub", help="stub / claude-cli / anthropic-api")
    ap.add_argument("--corpus", default=str(ROOT / "demo_data" / "past_projects"))
    ap.add_argument("--out", default=str(ROOT / "out"))
    args = ap.parse_args()

    t0 = time.time()
    report = {"provider": args.provider, "input": args.rfp}

    # 1) 読込
    raw = Path(args.rfp).read_text(encoding="utf-8")

    # 2) 脱敏(ローカル)
    masker = Masker(str(ROOT / "masking" / "entities.json"))
    masked, mapping = masker.mask(raw)
    report["masked_entities"] = mapping

    # 3) 類似先例検索(ローカルRAG)
    idx = BM25Index()
    idx.add_dir(args.corpus, "**/design_*.md")
    hits = idx.search(masked, k=2)
    report["references"] = [{"title": h["title"], "score": h["score"]} for h in hits]
    refs_text = "\n\n---\n\n".join(f"【{h['title']}】\n{h['text'][:2500]}" for h in hits) or "(先例なし)"

    # 4) LLM起草(クラウド脳。渡るのは伏せ字済みテキストのみ)
    provider = get_provider(args.provider)
    prompt = PROMPT_TEMPLATE.format(references=refs_text, requirements=masked)
    draft = provider.complete(prompt)

    # 5) 構造検査(ローカル質検)
    qc = check(draft, known_real_names=list(mapping.keys()))
    report["qc"] = qc
    report["elapsed_sec"] = round(time.time() - t0, 1)

    # 6) 出力
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.rfp).stem
    draft_path = outdir / f"{stem}_draft.md"
    draft_path.write_text(draft, encoding="utf-8")
    (outdir / f"{stem}_masked.md").write_text(masked, encoding="utf-8")
    (outdir / f"{stem}_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] draft -> {draft_path}")
    print(f"     masked entities: {len(mapping)} | refs: {[h['title'] for h in hits]}")
    print(f"     QC: {'PASS' if qc['ok'] else 'FINDINGS: ' + '; '.join(qc['findings'])}")
    print(f"     elapsed: {report['elapsed_sec']}s (provider={args.provider})")


if __name__ == "__main__":
    main()
