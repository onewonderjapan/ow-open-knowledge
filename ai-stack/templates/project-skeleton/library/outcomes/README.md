# Outcomes 結果庫

> 全生成/全実行を1行JSONで記録（append-only、成功も失敗も）。
> 目的: 次の生成前に同型の成功例をgrepしてfew-shotに使い、敗例のfailure_modeから対策を事前注入する。

## Schema（プロジェクトに合わせて確定してから運用開始）

```json
{
  "date": "YYYY-MM-DD",
  "task": "<対象の識別子>",
  "take": "v1",
  "method": "<生成方式/モデル>",
  "spec_ref": "<プロンプト/指示の所在ファイル#anchor>",
  "verdict": "accept | provisional | reject",
  "failure_modes": [],
  "notes": "<勝ち筋/敗因を一言>"
}
```

## failure_modes 標準語彙（STARTUP標準§3の領域別表から選んで確定。追加はここに先に書く）

<領域語彙をここへ>

## 規則

- QC担当が判定のたびに1行追記（漏れ=QC工程違反）
- 過去行は編集しない。訂正は新しい行+notes
