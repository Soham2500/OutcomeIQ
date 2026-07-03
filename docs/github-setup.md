# OutcomeIQ — GitHub Setup Guide

This guide prepares the OutcomeIQ repository for its first GitHub push. Run commands from:

```text
C:\Users\soham\OneDrive\Documents\pro
```

## 1. Initialize Git

```powershell
git init
```

If `.git` already exists, this command is safe but unnecessary.

## 2. Verify Ignore Rules Before Staging

Check that the virtual environment and local secrets are ignored:

```powershell
git check-ignore -v .venv
git check-ignore -v backend\.env
```

Check that source and examples remain trackable:

```powershell
git check-ignore backend\.env.example
git check-ignore README.md
git check-ignore docs\product-understanding.md
git check-ignore scripts\day2_verify.ps1
```

The second group should produce no ignore-rule output.

## 3. Review Repository Status

```powershell
git status
```

Confirm `.venv`, `.env`, caches and secrets are absent from the untracked-file list.

## 4. Stage Project Files

```powershell
git add .
```

Review what will be committed:

```powershell
git status
```

For a more detailed staged-file review:

```powershell
git diff --cached --name-status
```

## 5. Create the First Commit

```powershell
git commit -m "day-1-2: setup OutcomeIQ documentation and backend foundation"
```

## 6. Create the GitHub Repository Manually

1. Sign in to GitHub.
2. Select **New repository**.
3. Choose a repository name such as `outcomeiq`.
4. Add an optional description.
5. Choose public or private visibility.
6. Do not initialize it with a README, `.gitignore` or license because those files already exist locally.
7. Create the repository and copy its HTTPS or SSH URL.

## 7. Connect the Remote

Rename the local branch to `main`:

```powershell
git branch -M main
```

Add the GitHub repository as `origin`:

```powershell
git remote add origin <your-github-repo-url>
```

Verify the remote:

```powershell
git remote -v
```

If `origin` already exists, inspect it before changing anything. Use `git remote set-url origin <your-github-repo-url>` only when the existing URL is known to be incorrect.

## 8. Push the Main Branch

```powershell
git push -u origin main
```

GitHub may request browser, token or SSH authentication depending on the selected remote URL.

## Files That Must Not Be Committed

- `.venv/` or any virtual environment
- `.env` or environment-specific secret files
- Passwords, API keys, JWT secrets or database credentials
- Python `__pycache__` and `.pyc` files
- `.pytest_cache`
- IDE-local folders
- Logs and build output
- Future `node_modules/`

## Files That Should Be Committed

- `.env.example`
- `README.md` files
- `docs/`
- `backend/`
- `scripts/`
- `.gitignore`
- Dockerfile and Docker Compose configuration
- Tests and requirements

## Final Safety Check

Before every push, run:

```powershell
git status
git diff --cached
```

If a secret was staged, unstage it before committing and rotate the secret if it was ever pushed to a remote repository.
