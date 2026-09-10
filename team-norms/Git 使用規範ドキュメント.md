# Git 使用規範ドキュメント

## 1. ブランチ管理規範

### 1.1 ブランチの種類と命名規則

| ブランチ種類   | 命名形式                | 例                    | 説明                                            |
|:-------- |:------------------- |:-------------------- |:--------------------------------------------- |
| メインブランチ  | `main` または `master` | `main`               | 本番環境の安定コード。マージのみ許可、直接コミット禁止                   |
| 開発ブランチ   | `develop`           | `develop`            | 統合ブランチ。すべての機能は最終的にここにマージ                      |
| 機能ブランチ   | `feature/機能名`       | `feature/user-login` | 新機能開発。`develop` から分岐                          |
| 修正ブランチ   | `hotfix/問題概要`       | `hotfix/login-error` | 緊急修正。`main` から分岐し、修正後 `main` と `develop` にマージ |
| リリースブランチ | `release/バージョン番号`   | `release/v1.2.0`     | 新バージョンリリース準備。バグ修正やドキュメント更新のみ                  |
| 個人実験ブランチ | `exp/名前/説明`         | `exp/zhang/refactor` | 個人用実験コード。マージは強制しない                            |

### 1.2 ブランチ操作ルール

- **`main` / `develop` への直接コミットは禁止**
- すべての開発は `develop` をベースに `feature` ブランチを作成すること
- 機能完了後は **Pull Request (PR)** を通じて `develop` にマージすること
- PR は少なくとも 1 名以上のメンバーによるレビュー必須（個人プロジェクトは省略可）
- マージ前に CI（継続的インテグレーション）テストが成功していること

---

## 2. コミットメッセージ規範

### 2.1 形式

<タイプ>: <簡潔な説明>

### 2.2 タイプ一覧

| タイプ        | 説明                  |
| ---------- | ------------------- |
| `feat`     | 新機能                 |
| `fix`      | バグ修正                |
| `docs`     | ドキュメント修正            |
| `style`    | コード形式（機能に影響なし）      |
| `refactor` | リファクタリング（機能・バグ修正以外） |
| `perf`     | パフォーマンス改善           |
| `test`     | テスト追加・修正            |
| `chore`    | ビルドプロセスや補助ツールの変更    |

### 2.3 例

```text
feat: ログイン機能を追加
```

```text
fix: 商品数量が負数の場合の合計金額計算エラーを修正

```

## 3. Rebase 操作手順（完全ガイド）

この章では `git rebase -i` を使用してコミットを結合する方法と、競合の処理方法を詳しく説明します。

### 3.1 準備作業

```bash
# 1. 現在のブランチを確認
git branch

# 2. ワークスペースがクリーンであることを確認（未コミットの変更がないこと）
git status

# 3. 未コミットの変更がある場合は、一時退避またはコミット
git stash        # 変更を一時退避
# または
git add . && git commit -m "一時保存"
```

### 3.2 develop と同期してコミットを結合

```bash
# 1. 最新の develop コードを取得
git fetch origin develop

# 2. 現在のブランチを develop にリベース（履歴を線形に保つ）
git rebase origin/develop
```

### 3.3 複数コミットの結合

```bash
# 方式1：最近の n 個のコミットを結合（推奨）
git rebase -i HEAD~n   # n は結合するコミット数

# 方式2：develop から分岐したすべてのコミットを結合
git rebase -i origin/develop
```

### 3.4 インタラクティブモードの操作説明

上記コマンド実行後、テキストエディタ（デフォルトは vim）が開き、以下のような内容が表示されます：

```bash
pick abc1234 feat: 決済インターフェースを追加
pick def5678 fix: 署名パラメータのエラーを修正
pick ghi9012 style: コード形式を調整
pick jkl3456 test: 単体テストを追加

# Rebase 1234567..abcdefg onto 9876543 (4 commands)
#
# Commands:
# p, pick = このコミットを使用
# r, reword = このコミットを使用し、コミットメッセージを変更
# e, edit = このコミットを使用し、内容を修正するために一時停止
# s, squash = このコミットを使用し、前のコミットに結合
# f, fixup = squash と同じだが、コミットメッセージは破棄
# d, drop = このコミットを削除
#
# 注意：1行目は squash/fixup に変更できない
```

**操作手順**：

1. **最初のコミットは `pick` のままにしておく**（変更不可）

2. **結合したい後続のコミットの `pick` を `squash`（または `s`）に変更する**

3. **保存して終了**（vim では `Esc` を押してから `:wq`）

変更後の例：

```text
pick abc1234 feat: 決済インターフェースを追加
squash def5678 fix: 署名パラメータのエラーを修正
squash ghi9012 style: コード形式を調整
squash jkl3456 test: 単体テストを追加
```

### 3.5 最終的なコミットメッセージを編集

保存後、再びエディタが開き、結合後の最終コミットメッセージを編集します：

```bash
# This is a combination of 4 commits.
# This is the 1st commit message:

feat: 決済インターフェースを追加

# This is the 2nd commit message:

fix: 署名パラメータのエラーを修正

# This is the 3rd commit message:

style: コード形式を調整

# This is the 4th commit message:

test: 単体テストを追加
```

**操作**：

- 不要な行を削除し、明確で完全なコミットメッセージだけを残す

- 推奨形式：

```text
feat: 決済機能を実装

- SDKの依存関係を追加
- 署名検証ロジックを実装
- 単体テストを追加
```

保存して終了すると rebase が完了します。

### 3.6 競合の処理（発生した場合）

rebase 中に競合が発生した場合：

```bash
# 1. 競合ファイルを確認
git status

# 2. 競合ファイルを手動で編集し、競合を解決
#    <<<<<<<、=======、>>>>>>> のマーカーを削除

# 3. 解決したことをマーク
git add <競合ファイル>

# 4. rebase を継続
git rebase --continue

# 5. すべての競合が解決されるまで上記を繰り返す
```

**ebase を中止する**（競合が複雑な場合）：

```bash
git rebase --abort
```

### 3.7 リモートブランチへプッシュ

```bash
# --force-with-lease を使用して強制プッシュ（より安全）
git push --force-with-lease origin <ブランチ名>

# 例
git push --force-with-lease origin feature/payment
```

### 3.8 完全な操作フロー（クイックリファレンス）

```text
# 1. ワークスペースがクリーンであることを確認
git status

# 2. 最新の develop を取得
git fetch origin develop

# 3. develop にリベース
git rebase origin/develop

# 4. コミットを結合（例：最近の4個を結合）
git rebase -i HEAD~4

# 5. 編集：最初を pick、残りを squash に変更 → 保存

# 6. 最終的なコミットメッセージを編集 → 保存

# 7. 競合があれば、解決後に git add . && git rebase --continue

# 8. 強制プッシュ
git push --force-with-lease origin <ブランチ名>
```

## 4. ワークフロー例

### 4.1 新機能の開発

```bash
# 1. 最新の develop を取得
git checkout develop
git pull origin develop

# 2. 機能ブランチを作成
git checkout -b feature/payment

# 3. 開発中に複数回コミット（コミット規範に従う）
git add .
git commit -m "feat(payment): SDKの依存関係を追加"
git commit -m "fix(payment): 署名パラメータのエラーを修正"
git commit -m "style(payment): コード形式を調整"
# ... 開発継続 ...

# 4. 機能完了後、リモートにプッシュ
git push origin feature/payment
```

### 4.2 レビュー前のコミット結合

```bash
# 1. 機能ブランチにいることを確認
git checkout feature/payment

# 2. rebase を実行してコミットを結合（第3章の完全手順を参照）
git fetch origin develop
git rebase origin/develop
git rebase -i HEAD~5   # 最近5個のコミットを結合

# 3. 強制プッシュ
git push --force-with-lease origin feature/payment

# 4. Pull Request を発行
```

### 4.3 レビュー否決後の修正と再 Rebase

```bash
# 1. レビュー意見に基づいてコードを修正
git add .
git commit -m "fix(payment): レビュー意見に基づき署名検証ロジックを修正"

# 2. 再度 rebase を実行（新しいコミットを結合）
git fetch origin develop
git rebase origin/develop
git rebase -i HEAD~2   # 元の1個 + 新規1個 = 2個と仮定

# 3. インタラクティブ画面で、新しいコミットを squash に設定

# 4. 強制プッシュ
git push --force-with-lease origin feature/payment

# 5. PR でレビュー意見に返信
```

### 4.4 緊急修正（ホットフィックス）

```bash
# 1. main から hotfix ブランチを作成
git checkout main
git pull origin main
git checkout -b hotfix/price-error

# 2. 修正してコミット
git commit -m "fix(price): 割引計算エラーを修正"

# 3. main にマージ
git checkout main
git merge --no-ff hotfix/price-error

# 4. develop に同期
git checkout develop
git merge --no-ff hotfix/price-error

# 5. hotfix ブランチを削除
git branch -d hotfix/price-error
```

## 5. 禁止行為と注意事項

- ❌ 共有ブランチ（main/develop）への強制プッシュ (`git push --force`)

- ❌ 大きなバイナリファイル（>5MB）や機密情報（パスワード、キー）のコミット

- ❌ テスト未実行やコンパイルエラーがあるコードのコミット

- ❌ 共有ブランチでの `git reset` 後の強制プッシュ

- ✅ **Pull Request 発行前に、rebase を使用して機能ブランチ上の複数コミットを意味のある少数のコミットに結合すること**

- ✅ **PR レビュー否決後に修正した場合、修正後は再度 rebase を実行し、新しいコミットを結合（または既存のコミットに統合）して、コミット履歴をクリーンに保つこと**

- ✅ 定期的に `git pull --rebase` を実行してコミット履歴を線形に保つ（個人ブランチは柔軟に）

- ✅ `.gitignore` を使用して一時ファイルやローカル設定を無視する



## 付録：Rebase よくある質問（FAQ）

### Q1：現在のブランチのコミット数を確認する方法は？

```bash
git log --oneline | wc -l
#または

git rev-list --count HEAD
```



### Q2：結合する数を間違えた場合の対処法は？

```bash
# エディタ内の場合は、そのままキャンセル（vim では :q!）

# 保存してしまいまだ続行していない場合は、以下を実行：

git rebase --abort # 今回の rebase を中止し、元の状態に戻す
```



### Q3：すでにリモートにプッシュした後、rebase 後に push が拒否された場合の対処法は？

```bash
# 強制プッシュを使用（他の人がこのブランチを使っていないことを確認）

git push --force-with-lease origin <ブランチ名>
```

 

### Q4：誤って他人のコミットまで squash してしまった場合の対処法は？

```bash
# reflog を使用して復元

git reflog
git reset --hard <元のコミットハッシュ>
```



### Q5：小さな修正を前のコミットに直接結合したい場合の方法は？

```bash
git add .
git commit --amend --no-edit # 前のコミットに結合、元のメッセージを保持

# または

git commit --amend -m "新しいコミットメッセージ"
```




