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
from pipeline.drafting import PROMPT_TEMPLATE, build_prompt, build_references   # noqa: E402,F401


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
    report["masked_entity_count"] = len(mapping)
    report["masked_labels"] = list(mapping.values())

    # 3) 類似先例検索(ローカルRAG)
    idx = BM25Index()
    idx.add_dir(args.corpus, "**/design_*.md")
    hits = idx.search(masked, k=2)
    # 先例文書も脱敏する。要件書だけ脱敏してここを素通りさせると実名が出境する
    refs_text, mapping = build_references(hits, masker, mapping)
    report["references"] = [{"title": h["title"], "score": h["score"]} for h in hits]

    # 4) LLM起草(クラウド脳。渡るのは伏せ字済みテキストのみ)
    provider = get_provider(args.provider)
    draft = provider.complete(build_prompt(masked, refs_text))

    # 5) 構造検査(ローカル質検)
    qc = check(draft, known_real_names=list(mapping.keys()))
    report["qc"] = qc
    report["elapsed_sec"] = round(time.time() - t0, 1)

    # 6) 出力
    outdir = Path(args.out); outdir.mkdir(exist_ok=True)
    stem = Path(args.rfp).stem
    (outdir / f"{stem}_draft.md").write_text(draft, encoding="utf-8")
    (outdir / f"{stem}_masked.md").write_text(masked, encoding="utf-8")
    (outdir / f"{stem}_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / f"{stem}_mapping.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[OK] draft -> {outdir / f'{stem}_draft.md'}")
    print(f"     masked entities: {len(mapping)} | refs: {[h['title'] for h in hits]}")
    print(f"     QC: {'PASS' if qc['ok'] else 'FINDINGS: ' + '; '.join(qc['findings'])}")
    print(f"     elapsed: {report['elapsed_sec']}s (provider={args.provider})")
    print(f"     mapping (do not publish): {outdir / f'{stem}_mapping.json'}")


if __name__ == "__main__":
    main()
