---
title: Git 功能速查 — Codex 試跑用到的指令
tags: [git, codex, course-note, 紡織所]
created: 2026-07-12
modified: 2026-07-12
---
# Git 功能速查 — Codex 試跑用到的指令

這份筆記記錄這次 Codex 三小時課程 dry run 裡實際用到的 Git 功能。重點不是完整教 Git，而是知道在 AI coding agent 試跑時，每個指令扮演什麼安全角色。

## 1. `git clone`：複製遠端專案

```bash
git clone https://github.com/ChienTony/codex-textile-demo.git
cd codex-textile-demo
```

用途：把 GitHub 上的正式 demo repo 複製到本機，建立一份可操作的工作副本。

在課程 dry run 裡，這一步用來模擬學員拿到教材的真實流程。建議每次正式試跑都用乾淨資料夾重新 clone，避免被舊變更干擾。

## 2. `git checkout <branch>`：切換分支

```bash
git checkout starter
git checkout solution
```

用途：切換到不同版本的專案狀態。

這次用到的分支：

- `starter`：學員起點，保留 blank `yards` crash bug。
- `solution`：講師參考答案，測試與 CLI smoke 都應通過。

注意：如果目前工作目錄有未提交變更，而且切換分支可能覆蓋那些變更，Git 會中止 checkout。這次就遇到：

```text
error: Your local changes to the following files would be overwritten by checkout
```

這是 Git 在保護你，避免把 Codex 剛改出的成果覆蓋掉。

## 3. `git status`：檢查目前工作區狀態

```bash
git status
```

用途：確認現在在哪個分支、有哪些檔案被修改、工作目錄是否乾淨。

常見輸出：

```text
On branch starter
Your branch is up to date with 'origin/starter'.

nothing to commit, working tree clean
```

這表示：

- 目前在 `starter` 分支。
- 本地分支與遠端 `origin/starter` 同步。
- 沒有未提交變更。

在 AI agent 工作流裡，`git status` 是最重要的安全檢查之一：

- Codex 執行前看一次，確認起點乾淨。
- Codex 執行後看一次，確認它到底有沒有改檔案。
- 切換分支前看一次，避免不小心覆蓋變更。

## 4. `git diff --stat`：快速看改了哪些檔案

```bash
git diff --stat
```

用途：用摘要方式看這次變更影響哪些檔案、增刪多少行。

這次 Codex 解法的摘要是：

```text
src/order_summary.py        | 19 +++++++++++++++++--
tests/test_order_summary.py | 15 +++++++++++++++
2 files changed, 32 insertions(+), 2 deletions(-)
```

這代表 Codex 只改了：

- 主程式：`src/order_summary.py`
- 測試：`tests/test_order_summary.py`

這很符合任務範圍，因為這次目標就是修 bug 並補測試。

## 5. `git diff`：看完整變更內容

```bash
git diff
```

用途：查看每一行實際改了什麼。

`git diff --stat` 只告訴你「改了哪些檔案」；`git diff` 才能確認「改法是否合理」。

這次用它檢查 Codex 解法是否包含：

- 空白 `yards` / `unit_price` 的略過與警告處理
- 非整數數值的錯誤處理
- 空白 `yards` 的回歸測試

在 Codex 課程中可以強調：

> Codex 說它改了什麼不算數，`git diff` 才是實際發生的事。

## 6. `git stash push -m "..."`：暫存目前變更

```bash
git stash push -m "WIP: blank yards fix"
```

用途：把目前工作目錄的未提交變更收起來，讓工作目錄回到乾淨狀態。

這次使用 stash 的原因是：Codex 已經在 `starter` 上產生修 bug 變更，但要切到 `solution` 分支做對照驗證。直接 checkout 會被 Git 阻止，所以先 stash。

效果：

- Codex 解法沒有被刪除。
- 工作目錄變乾淨。
- 可以安全切換到 `solution`。

這比直接 `git restore .` 安全，因為 stash 是可回復的。

## 7. `git stash list`：列出所有 stash

```bash
git stash list
```

用途：查看目前保存了哪些暫存變更。

這次的 stash 是：

```text
stash@{0}: On starter: WIP: blank yards fix
```

意思是：

- `stash@{0}`：最新一筆 stash。
- `On starter`：是在 `starter` 分支上存的。
- `WIP: blank yards fix`：當時指定的說明文字。

## 8. `git stash show --stat stash@{0}`：看 stash 摘要

```bash
git stash show --stat stash@{0}
```

用途：不套用 stash，只看它改了哪些檔案、增刪多少行。

這很適合用在不想污染目前工作目錄、但想先確認 stash 內容的時候。

## 9. `git stash show -p stash@{0}`：看 stash 完整差異

```bash
git stash show -p stash@{0}
```

用途：不套用 stash，直接查看 stash 內完整 patch。

這次用它確認 Codex 的解法內容，且 stash 仍然保留，沒有套用也沒有刪除。

這是一個很適合講師課前檢查的安全用法：

```text
先看 stash 內容，不急著套回工作目錄。
```

## 10. `git stash apply stash@{0}`：套用 stash，但保留 stash

```bash
git stash apply stash@{0}
```

用途：把 stash 裡的變更套回目前工作目錄，但 stash 本身仍保留。

適合情境：你想重新測 Codex 解法，但又不想失去這份 stash 備份。

套用後可以執行：

```bash
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

看完後若要回到乾淨狀態：

```bash
git restore .
git status
```

## 11. `git stash pop`：套用 stash，並刪除 stash

```bash
git stash pop
```

用途：把 stash 套回工作目錄，成功後從 stash list 移除。

注意：課前 dry run 通常不建議一開始用 `pop`，因為它會消耗掉 stash。比較保守的流程是先用：

```bash
git stash apply stash@{0}
```

確認沒問題後，再決定要不要刪。

## 12. `git stash drop stash@{0}`：刪除指定 stash

```bash
git stash drop stash@{0}
```

用途：確認不再需要某份 stash 後，把它刪掉。

這次建議先不要刪，因為 `stash@{0}` 可以保留作為：

- Codex 現場解法樣本
- 與 `solution` 分支的對照材料
- 課堂上說明「AI 解法 vs 參考答案」的例子

## 13. `git restore .`：捨棄工作目錄變更

```bash
git restore .
```

用途：把目前工作目錄中被修改的追蹤檔案還原成 Git 記錄中的版本。

這次在看完 stash diff 後執行：

```bash
git restore .
git status
```

結果回到：

```text
On branch starter
Your branch is up to date with 'origin/starter'.

nothing to commit, working tree clean
```

注意：`git restore .` 會丟掉目前工作目錄的變更，所以只有在確認變更已經 stash、commit，或確定不需要時才使用。

## 14. `origin/starter`、`origin/solution`：遠端追蹤分支

當 `git status` 顯示：

```text
Your branch is up to date with 'origin/starter'.
```

意思是本地 `starter` 分支目前和 GitHub 遠端的 `starter` 分支一致。

這次也看到 `solution` 正在追蹤 `origin/solution`，代表本地 `solution` 不是孤立分支，而是對應 GitHub 上的正式參考答案分支。

## 15. 這次 dry run 的 Git 安全節奏

可以把這次流程整理成：

```text
clone 正式 repo
→ checkout starter
→ status 確認乾淨
→ Codex 修改
→ diff / diff --stat 檢查實際變更
→ stash 保存 Codex 解法
→ checkout solution
→ 跑測試與 CLI smoke
→ checkout starter
→ stash show 檢查 Codex 解法
→ restore 回乾淨 starter
→ status 確認乾淨
```

核心觀念：

1. **先確認起點乾淨**：`git status`
2. **讓 Codex 修改後一定看 diff**：`git diff --stat`、`git diff`
3. **想保留但暫時不用的變更先 stash**：`git stash push -m "..."`
4. **要丟掉工作目錄變更才用 restore**：`git restore .`
5. **切分支前先處理未提交變更**：避免 checkout 被 Git 阻止，也避免覆蓋成果

## 16. 對 Codex 課程的講法

可以用一句話總結給學員：

> Git 是 AI coding agent 的安全網。Codex 可以幫你改，但你要用 `status`、`diff`、`stash`、`restore` 控制現場，確認每一步真的發生了什麼。
