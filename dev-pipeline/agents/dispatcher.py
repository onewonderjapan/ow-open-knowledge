"""Dispatcher Agent - 要件を分類し、適切なパイプラインを決定."""

from __future__ import annotations

from agents.base import BaseAgent
from core.config import Config
from core.models import DispatchResult, WorkType

SYSTEM_PROMPT = """\
あなたは AI Agent パイプラインのディスパッチャーです。
ユーザーの要件を分析し、作業種別を判定してください。

## 作業種別の定義

1. **development** (機能開発)
   - コードの新規作成・修正が主目的
   - API / UI / CLI ツール / スクリプト等の実装
   - Git リポジトリが指定されている場合が多い
   - 例: 「TODO API を作成」「ログイン機能を追加」「バグ修正」

2. **infrastructure** (基盤構築)
   - サーバ / ネットワーク / クラウド基盤の設計書作成が主目的
   - 構築手順書、設定仕様書、移行計画書などのドキュメント生成
   - 実装よりも設計・計画が中心
   - 例: 「MCC サーバの設計書を作成」「ネットワーク移行計画」「Intune 設定仕様書」

3. **investigation** (調査)
   - 技術調査、比較検討、実現性分析が主目的
   - コードやインフラの構築は不要
   - レポート・報告書の作成のみ
   - 例: 「Azure vs AWS の比較」「MCC 導入調査」「セキュリティリスク調査」

4. **design_review** (設計レビュー)
   - 既存の設計書や計画書のレビュー・補強が主目的
   - 新規作成ではなく、既存ドキュメントの改善
   - 例: 「設計書のレビュー」「テスト計画の見直し」

## 各作業種別のパイプライン

- development: investigator → analyst → developer → tester → investigator(問題調査)
- infrastructure: investigator → analyst → developer → tester → investigator(問題調査)
- investigation: investigator のみ
- design_review: analyst → developer

## 出力形式

JSON のみ出力してください：
```json
{
  "work_type": "development|infrastructure|investigation|design_review",
  "label": "日本語ラベル（機能開発/基盤構築/調査/設計レビュー）",
  "reason": "判断理由を1-2文で",
  "pipeline": ["investigator", "analyst", "developer", "tester", "investigator_post"],
  "notes": "補足事項（あれば）"
}
```
"""

# 作業種別ラベル
WORK_TYPE_LABELS = {
    WorkType.DEVELOPMENT: "機能開発",
    WorkType.INFRASTRUCTURE: "基盤構築",
    WorkType.INVESTIGATION: "調査",
    WorkType.DESIGN_REVIEW: "設計レビュー",
}

# 作業種別ごとのデフォルトパイプライン
DEFAULT_PIPELINES = {
    WorkType.DEVELOPMENT: ["investigator", "analyst", "developer", "tester", "investigator_post"],
    WorkType.INFRASTRUCTURE: ["investigator", "analyst", "developer", "tester", "investigator_post"],
    WorkType.INVESTIGATION: ["investigator"],
    WorkType.DESIGN_REVIEW: ["analyst", "developer"],
}


class DispatcherAgent(BaseAgent):
    """要件分類 Agent：要件を分析し、適切なパイプラインを決定."""

    name = "dispatcher"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def classify(self, requirement: str) -> DispatchResult:
        """要件を分類し、DispatchResult を返す."""
        self.logger.info("要件を分類中...")

        prompt = self.load_evolved_prompt(SYSTEM_PROMPT)
        data = self.call_llm_json(prompt, requirement)

        try:
            work_type = WorkType(data["work_type"])
        except (KeyError, ValueError):
            self.logger.warning(f"  不明な work_type: {data.get('work_type')}、development にフォールバック")
            work_type = WorkType.DEVELOPMENT

        pipeline = data.get("pipeline", DEFAULT_PIPELINES[work_type])
        label = data.get("label", WORK_TYPE_LABELS.get(work_type, "不明"))

        result = DispatchResult(
            work_type=work_type,
            label=label,
            reason=data.get("reason", ""),
            pipeline=pipeline,
            notes=data.get("notes", ""),
        )

        self.logger.info(f"  -> 種別: {result.label} ({result.work_type.value})")
        self.logger.info(f"  -> 理由: {result.reason}")
        self.logger.info(f"  -> パイプライン: {' → '.join(result.pipeline)}")

        # 結果を保存
        output_dir = self.config.output_dir / "dispatcher"
        output_dir.mkdir(parents=True, exist_ok=True)
        result.save(output_dir / "dispatch.json")

        return result
