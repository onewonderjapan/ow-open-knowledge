# ai-stack 開発ガイド（Claude向け）

企業AI導入提案の参考実装。構想と提案資料（社内）は公開範囲外のため本リポジトリには含まれない。

## 原則
- **各層のインターフェースを壊さない**: masking.Masker.mask / rag.*.search / llm.get_provider /
  evalkit.check のシグネチャは薄切片→本格版の差し替え契約。上位層を巻き込む変更は要相談。
- **デモデータは架空のみ**: 実在の企業名・人名・案件を demo_data/ に入れない。
- 脱敏層のテストを書かずに脱敏ルールを変更しない（漏れ=事故）。`ai-stack/tests/test_masker.py`。
- 踩んだ坑は必ず `../agent-cultivation/PITFALLS.md` に追記（日本語）。
- Python はプロジェクトの `.venv` を使う（システムPythonに入れない）。
  POSIX: `.venv/bin/python` / Windows: `.venv/Scripts/python.exe`
- コミットメッセージは日本語可。
- オフライン検証: リポジトリルートで `python scripts/verify.py`

## 環境メモ
- Windows 11 / Python 3.13 / CJKユーザー名 → HuggingFace系を使う時は `HF_HOME=C:\hf_cache` 必須
- `claude-cli` プロバイダは Claude Code の `-p` を子プロセス起動（サブスク認証流用、PoC専用）
