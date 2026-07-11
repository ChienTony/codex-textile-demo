# codex-textile-demo

A tiny textile-order reporting project for the Codex three-hour hands-on course.

## 課堂中不知道下一步怎麼操作？

請先打開：

- [SHELL-CHEATSHEET.md](./SHELL-CHEATSHEET.md)：課堂階段式 shell 指令速查
- [Git功能速查-Codex試跑.md](./Git功能速查-Codex試跑.md)：這次 Codex 試跑用到的 Git 安全操作

這些檔案依照課程與試跑流程整理了可直接複製的指令。
如果你卡住，請不要自己亂猜，先回到對應階段照著操作。

The project intentionally stays small so learners can focus on the Codex workflow:

1. Ask Codex to understand the repo before changing files.
2. Ask for a plan before edits.
3. Review `git diff` after edits.
4. Run tests or a smoke command to verify behavior.

## Scenario

`sample_data/orders.csv` contains fabric orders with customer, fabric, color, yards, and unit price.

The script in `src/order_summary.py` reads the CSV and prints a small order summary.

One row intentionally has a blank `yards` value. The desired behavior is to skip invalid rows and report a warning instead of crashing.

## Course branches

This repository is used with two local teaching branches:

- `starter`: intentionally contains the blank-`yards` bug for the hands-on exercise.
- `solution` / `main`: contains the completed reference implementation.

For the course exercise, start from the buggy branch:

```bash
git checkout starter
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

The unit tests on `starter` are intentionally incomplete and may pass before the bug is fixed. The CLI smoke command is expected to reveal the problem until learners add a regression test and fix the code.

To compare with the reference answer later:

```bash
git checkout solution
python3 src/order_summary.py sample_data/orders.csv
python3 -m unittest discover -s tests -v
```

## Quick start

On the completed `main` / `solution` branch:

```bash
python3 src/order_summary.py sample_data/orders.csv
python3 -m unittest discover -s tests -v
```

## Suggested Codex prompts

### 1. Understand the repo

```text
請閱讀這個 repo，告訴我它是做什麼的。
請用非工程背景也聽得懂的方式說明。
先不要修改任何檔案。
```

### 2. Fix a bug

```text
目前程式遇到 orders.csv 裡 yards 欄位是空白時應該跳過該列並回報 warning。
請先說明可能原因，然後提出修法。
在我確認前不要修改檔案。
```

### 3. Add a feature

```text
請新增一個功能：依 customer 統計總 yards。
請先寫測試，再修改程式，最後告訴我怎麼驗證。
```

### 4. Code review

```text
請 review 這個 repo。
請找出可讀性、錯誤處理、測試覆蓋率、文件清楚度可以改善的地方。
先不要修改檔案，只列出建議，並依重要性排序。
```
