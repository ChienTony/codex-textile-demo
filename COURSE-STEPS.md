# Codex Textile Demo 操作步驟

## 第一步

```powershell
git checkout starter
git status
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

## 第二步

```powershell
codex exec "Task: Improve README.md by adding a short 'How to verify' section for this textile order summary project. Scope: Only modify README.md. Constraints: Do not modify src/order_summary.py, tests, or sample_data. Do not change the behavior of the project. Validation: After editing, tell me the exact commands a learner should run: python3 -m unittest discover -s tests -v and python3 src/order_summary.py sample_data/orders.csv. Output: Report changed files and any assumptions."
```

## 第三步

```powershell
git status
git diff --stat
git diff
python3 -m unittest discover -s tests -v
```

## 第四步

```powershell
git restore README.md
git status
```

## 第五步

```powershell
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

## 第六步

```powershell
codex exec "Task: Fix the bug where src/order_summary.py crashes when orders.csv contains a blank yards field. Context: sample_data/orders.csv includes order A004 with a blank yards value. The program should skip invalid numeric rows and report a warning instead of crashing. Scope: You may modify src/order_summary.py and tests/test_order_summary.py. Constraints: Do not change the CSV column names. Do not change the CLI command. Do not add third-party dependencies. Do not rewrite unrelated code. Validation: Add or update a unittest case for blank yards. Run: python3 -m unittest discover -s tests -v. Also run: python3 src/order_summary.py sample_data/orders.csv. Output: Report changed files, test results, CLI output summary, and any assumptions."
```

## 第七步

```powershell
git stash push -m "blank-yards-fix"
git checkout solution
python3 -m unittest discover -s tests -v
python3 src/order_summary.py sample_data/orders.csv
```

## 第八步

```powershell
git checkout starter
git stash show --stat 'stash@{0}'
git stash show -p 'stash@{0}'
```

