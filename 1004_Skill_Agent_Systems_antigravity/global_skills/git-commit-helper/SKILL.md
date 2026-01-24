---
name: git-commit-helper
description: Generates clear, conventional commit messages from git diffs.
tools: run_command
---

# Git Commit Helper

## Purpose
To streamline the git commit process by analyzing changes and generating standardized commit messages.

## Instructions
1.  **Check Status**: Run `git status` to see what is staged.
2.  **Verify Staged Changes**:
    -   If nothing is staged, ask the user what to stage or offer to `git add .`.
    -   If changes are staged, proceed to step 3.
3.  **Analyze Diff**: Run `git diff --staged` to read the actual changes.
4.  **Draft Message**: detailed commit message following **Conventional Commits** format:
    -   `type(scope): subject`
    -   (blank line)
    -   `body`
    -   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
5.  **Confirm & Commit**:
    -   Show the drafted message to the user.
    -   If approved, run `git commit -m "..."`.

## Examples
**Diff**: Added a new function `calculateTotal` in `cart.js`.
**Draft**:
```text
feat(cart): add calculateTotal function

Implement total calculation logic including tax and shipping.
```
