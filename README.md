# Nexus

Python project managed with [uv](https://docs.astral.sh/uv/).

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Python 3.14+ (uv can install it: `uv python install 3.14`)

## Setup

From the project root:

```bash
# Create / refresh the virtual environment (.venv)
uv venv

# Install dependencies from pyproject.toml / uv.lock
uv sync
```

`uv sync` creates `.venv` automatically if it is missing, so `uv venv` is optional after the first clone.

## Daily use

```bash
# Activate the venv (optional — uv run works without activation)
source .venv/bin/activate

# Run the app
uv run python main.py
# or, with venv activated:
python main.py

# Add a dependency
uv add requests

# Add a dev dependency
uv add --dev pytest ruff
```

## Cursor / VS Code

Select the interpreter: **`.venv/bin/python`** (Command Palette → “Python: Select Interpreter”).

# Add dependecies
uv add fastapi uvicorn anthropic pydantic-settings httpx python-dotenv
