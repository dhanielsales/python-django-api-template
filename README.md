# Development Environment Setup

## Recommended VS Code Extensions

To ensure code quality and consistency, please install the following VS Code extensions:

### 1. Ruff

- **Ruff** is a fast Python linter and code quality tool.
- **Install:**  
  [Ruff VS Code Extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- **Usage:**  
  The extension will automatically lint your code and show errors in the editor and Problems panel.  
  Configuration is managed via `pyproject.toml`.

### 2. Mypy Type Checker

- **Mypy** is a static type checker for Python.
- **Install:**  
  [Mypy Type Checker VS Code Extension](https://marketplace.visualstudio.com/items?itemName=matangover.mypy)
- **Usage:**  
  The extension will check type annotations and show errors in the editor and Problems panel.  
  Configuration is managed via `pyproject.toml`.

---

## Additional Recommendations

- **Python Extension:**  
  [Python (by Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)  
  This extension provides Python language support, code navigation, and debugging.

---

## Configuration

- Linting and type checking rules are defined in `pyproject.toml`.
- For strict type checking in VS Code, use `.vscode/settings.json`:
