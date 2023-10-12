# Jit - IDE pre-commit hooks


## Jit IDE Extension (VSCode) pre-commit hook
A pre-commit hook to use along with the IDE Extension.

[Getting Started with the pre-commit hook for Jit VSCode IDE Extension users](https://docs.jit.io/docs/jit-ide-extension-for-visual-studio#pre-commit-hook)

### Configuration
You can configure the pre-commit hook by modifying the parameters in the IDE Extension settings.


## Standalone IDE Pre-commit hooks


### Secrets Detection
A pre-commit hook to detect secrets in your code. This hook will scan the files you specify for secrets and block the commit if any are found.

### Getting Started
1. **Install `pre-commit`:**
   ```bash
   pip install pre-commit
   ```

2. **Create a `.pre-commit-config.yaml` in your repo:**
   ```yaml
   repos:
    - repo: https://github.com/jitsecurity/ide-pre-commit-hooks
      rev: 0.1.0
      hooks:
        - id: gitleaks
   ```

3. **Install the hook:**
   ```bash
   pre-commit install
   ```

4. **Commit changes:**
   When you commit, the `pre-commit` hook will automatically run.


## Usage
Once the pre-commit hook is installed and configured, it will automatically run whenever you try to commit changes to your repository. If there are findings in the specified file, the commit will be blocked and you will need to address the findings before committing again.
