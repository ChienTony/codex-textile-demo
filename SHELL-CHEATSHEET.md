# Shell 指令速查

這份文件是 Codex 三小時課程 hands-on 的操作速查。

如果你不知道下一步要輸入什麼，請：

1. 找到目前課程階段。
2. 複製對應指令。
3. 執行後觀察結果。
4. 如果結果和預期不同，立刻問講師，不要跳到下一步。

> 課堂原則：不要跨階段亂跳，尤其不要跳過 `git status`、`git diff`、測試指令。

## 給 Codex / Agent 的使用方式

如果你是 Codex 或其他 coding agent，請根據本檔案協助學員操作。

規則：

1. 不要跳過階段。
2. 每次修改前先確認 `git status`。
3. 修改後一定要求學員執行 `git diff` 與測試。
4. 如果學員卡住，先判斷他目前位於哪個階段，再只給下一個最小步驟。
5. 不要一次給太多指令。
6. 如果學員說「壞掉了」，先請他貼：
   - `git status`
   - 錯誤訊息
   - 他剛剛執行的指令

---

## 階段 0：安裝與登入確認

### 0-1. 安裝 Codex CLI

```bash
npm install -g @openai/codex
```

### 0-2. 確認 Codex 是否安裝成功

```bash
codex --version
```

### 0-3. 確認登入狀態

```bash
codex whoami
```

### 0-4. 如果尚未登入

一般環境：

```bash
codex login
```

如果是遠端、headless、瀏覽器不方便開的環境：

```bash
codex login --device-auth
```

---

## 階段 1：進入範例專案與確認 Git 狀態

這是所有 hands-on 開始前都要做的基本動作。

### 1-1. 進入範例專案

```bash
cd codex-textile-demo
```

### 1-2. 切到課程指定分支

```bash
git checkout starter
```

### 1-3. 確認目前工作區是否乾淨

```bash
git status
```

理想狀態應看到類似：

```text
nothing to commit, working tree clean
```

如果不是乾淨狀態，不要急著繼續，先請講師協助。

---

## 階段 2：第一次使用 Codex，只讀專案，不修改檔案

目標：先讓 Codex 理解專案，但明確要求它不要改檔案。

### 2-1. 執行只讀任務

```bash
codex exec "Read this project and summarize its structure. Explain what src/order_summary.py does, what sample_data/orders.csv contains, and how to run tests. Do not modify files."
```

### 2-2. Codex 跑完後，確認它真的沒有改檔案

```bash
git status
```

如果還是乾淨，才代表這次只讀任務沒有留下修改。

---

## 階段 3：小型 README 修改任務

目標：讓 Codex 做第一個低風險修改，只允許它改 README。

### 3-1. 請 Codex 只修改 README

```bash
codex exec "Task: Improve README.md by adding a short 'How to verify' section for this textile order summary project. Scope: Only modify README.md. Constraints: Do not modify src/order_summary.py, tests, or sample_data. Do not change the behavior of the project. Validation: After editing, tell me the exact commands a learner should run: python3 -m unittest discover -s tests -v and python3 src/order_summary.py sample_data/orders.csv. Output: Report changed files and any assumptions."
```

### 3-2. 修改後檢查 Git 狀態

```bash
git status
```

### 3-3. 看這次改了哪些檔案

```bash
git diff --stat
```

### 3-4. 看完整修改內容

```bash
git diff
```

### 3-5. 跑測試確認沒有壞掉

```bash
python3 -m unittest discover -s tests -v
```

---

## 階段 4：安全檢查與 rollback 指令

這一段不是新的功能任務，而是教學員「怎麼確認 Codex 改了什麼」與「必要時怎麼還原」。

### 4-1. 查看目前 Git 狀態

```bash
git status
```

### 4-2. 看修改摘要

```bash
git diff --stat
```

### 4-3. 看完整 diff

```bash
git diff
```

### 4-4. 如果要還原所有未提交修改

注意：這會把目前所有未提交修改都還原。如果你本來就有自己的修改，不要直接執行這行。

```bash
git restore .
```

### 4-5. 如果只要還原某個檔案

```bash
git restore path/to/file
```

範例：

```bash
git restore README.md
```

---

## 階段 5：修 bug 與補測試

目標：修正 `orders.csv` 中 `yards` 欄位空白時，CLI crash 的問題。

### 5-1. 重新確認分支與 Git 狀態

```bash
git checkout starter
git status
```

### 5-2. 先跑既有測試

```bash
python3 -m unittest discover -s tests -v
```

注意：這裡測試可能會通過，因為原本測試可能沒有覆蓋 blank `yards` 的情境。

### 5-3. 重現 CLI bug

```bash
python3 src/order_summary.py sample_data/orders.csv
```

如果 starter 分支還沒修過，這裡預期可能會 crash。

### 5-4. 請 Codex 修 bug 並補測試

```bash
codex exec "Task: Fix the bug where src/order_summary.py crashes when orders.csv contains a blank yards field. Context: sample_data/orders.csv includes order A004 with a blank yards value. The program should skip invalid numeric rows and report a warning instead of crashing. Scope: You may modify src/order_summary.py and tests/test_order_summary.py. Constraints: Do not change the CSV column names. Do not change the CLI command. Do not add third-party dependencies. Do not rewrite unrelated code. Validation: Add or update a unittest case for blank yards. Run: python3 -m unittest discover -s tests -v. Also run: python3 src/order_summary.py sample_data/orders.csv. Output: Report changed files, test results, CLI output summary, and any assumptions."
```

### 5-5. Codex 修改後，先看狀態

```bash
git status
```

### 5-6. 看改了哪些檔案

```bash
git diff --stat
```

### 5-7. 看完整修改內容

```bash
git diff
```

### 5-8. 跑 unittest

```bash
python3 -m unittest discover -s tests -v
```

### 5-9. 跑 CLI smoke test

```bash
python3 src/order_summary.py sample_data/orders.csv
```

預期結果應包含類似：

```text
Total orders: 5
Valid orders: 4
Total yards: 290
Total amount: 24800
Warnings:
- Skipped order A004: yards is blank
```

---

## 階段 6：測試失敗或修改太大時的處理

### 6-1. 如果測試失敗，請 Codex 檢查並修正

```bash
codex exec "The test suite is failing. Inspect the failure, fix the issue, and explain the root cause. Do not introduce unrelated changes."
```

修完後再次執行：

```bash
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

### 6-2. 如果 Codex 改太多，請它簡化修改

```bash
codex exec "Review your previous changes and simplify them. Keep the fix minimal and avoid unrelated refactoring."
```

之後再次檢查：

```bash
git diff --stat
git diff
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

### 6-3. 如果修改已經失控，只還原本次 bug fix 涉及檔案

```bash
git restore src/order_summary.py tests/test_order_summary.py
```

然後重新用更小、更清楚的 prompt 執行。

---

## 階段 7：Code Review 工作流

目標：Codex 改完後，不是直接相信，而是請它 review 目前的 git diff。

### 7-1. Review 前先確認目前狀態

```bash
git status
git diff --stat
git diff
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

### 7-2. 請 Codex review 目前 diff，但不要修改檔案

```bash
codex exec "請 review 我目前的 git diff。這次修改目標：修正 orders.csv 中 yards 欄位空白時程式 crash 的問題，並補上 blank yards 的 unittest。請先不要修改檔案，只輸出 review 結果。請依照以下分類：1. Correctness：這次修改是否真的解決問題？有沒有可能漏掉的邊界情境？2. Test coverage：目前測試是否足夠？還缺哪些測試？3. Scope control：這次修改是否有改到不相關的地方？4. Maintainability：程式碼是否容易理解與維護？5. Suggested next step：如果只能做一個後續動作，你建議做什麼？請每一點都簡短具體，不要泛泛而談。"
```

### 7-3. 如果 Codex 提到某個測試缺口，先請它解釋，不要立刻改

```bash
codex exec "你提到可能缺少 unit_price 非數字或 yards 只有空白的測試。請說明：1. 為什麼這個測試重要？2. 目前程式可能在哪裡出問題？3. 你建議新增哪一個最小測試案例？先不要修改檔案。"
```

### 7-4. 如果人類決定接受其中一項建議，再讓 Codex 小範圍修改

```bash
codex exec "請只新增你剛才建議的一個最小 CSV 邊界情境測試。限制：不要重構 production code；不要修改 sample_data/orders.csv；測試名稱要清楚表達情境；修改後請說明你改了哪裡。"
```

### 7-5. 修改後再次驗證

```bash
git status
git diff --stat
git diff
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

---

## 階段 8：常用 Codex 權限模式示範

給講師說明用，不建議初學者隨便切換高權限模式。

### 8-1. 預設模式

```bash
codex exec "Fix the failing test."
```

### 8-2. workspace-write 模式

適合任務明確，並且允許 Codex 在 workspace 內修改：

```bash
codex exec --sandbox workspace-write "Implement the todo validation feature and run tests."
```

### 8-3. danger-full-access 模式

高風險，不建議作為課堂預設：

```bash
codex exec --sandbox danger-full-access "Fix the test environment."
```

### 8-4. yolo 模式

只適合丟棄式 prototype，不建議正式專案使用：

```bash
codex exec --yolo "Build a quick throwaway prototype."
```

---

## 階段 9：如果學員不知道下一步，照這個最小安全流程走

這是課堂救援用流程。

```bash
git status
```

如果乾淨，再執行：

```bash
codex exec "Read this project and summarize how to run it and how to test it. Do not modify files."
```

Codex 回答後檢查：

```bash
git status
```

如果要開始修改，先用小任務，不要一次改太大：

```bash
codex exec "Please make one minimal change only. Before editing, explain what file you plan to modify and why. Do not rewrite unrelated code. After editing, report changed files and validation commands."
```

修改後固定檢查：

```bash
git status
git diff --stat
git diff
```

如果專案是這次課程的 `codex-textile-demo`，固定驗證：

```bash
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

---

## 階段 10：講師可貼給學員的「不要拖進度」版指令清單

如果現場時間緊，學員只需要照這組跑。

### A. 確認環境

```bash
codex --version
codex whoami
```

### B. 進入專案

```bash
cd codex-textile-demo
git checkout starter
git status
```

### C. 只讀理解專案

```bash
codex exec "Read this project and summarize its structure. Explain what src/order_summary.py does, what sample_data/orders.csv contains, and how to run tests. Do not modify files."
git status
```

### D. 跑測試與 CLI

```bash
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

### E. 修 bug

```bash
codex exec "Task: Fix the bug where src/order_summary.py crashes when orders.csv contains a blank yards field. Context: sample_data/orders.csv includes order A004 with a blank yards value. The program should skip invalid numeric rows and report a warning instead of crashing. Scope: You may modify src/order_summary.py and tests/test_order_summary.py. Constraints: Do not change the CSV column names. Do not change the CLI command. Do not add third-party dependencies. Do not rewrite unrelated code. Validation: Add or update a unittest case for blank yards. Run: python3 -m unittest discover -s tests -v. Also run: python3 src/order_summary.py sample_data/orders.csv. Output: Report changed files, test results, CLI output summary, and any assumptions."
```

### F. 檢查修改

```bash
git status
git diff --stat
git diff
```

### G. 驗證

```bash
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

### H. 如果壞掉，先不要亂改，請 Codex 分析

```bash
codex exec "The test suite or CLI command is failing. Inspect the failure, explain the root cause, and propose the smallest fix. Do not introduce unrelated changes."
```

### I. 如果修改失控，還原指定檔案

```bash
git restore src/order_summary.py tests/test_order_summary.py
```

---

## 給學員的三個固定規則

```text
1. Codex 前後都看 git status。
2. 有修改一定看 git diff。
3. 說「改好了」不算結束，測試與 CLI 跑過才算。
```
