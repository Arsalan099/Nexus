# Nexus
NEXUS — An Enterprise AI Knowledge Operating System
A mid-size company has years of internal knowledge trapped in documents, wikis, emails, reports, and databases. They want an AI system that can answer questions, synthesize information, take actions, and eventually operate autonomously on complex tasks — while being reliable, auditable, and cost-efficient.

NEXUS will evolve from a smart Q&A system into a full autonomous knowledge operating system.
The 10 Phases
Phase 1:  Foundation — Intelligent Assistant with Clean Architecture
Phase 2:  RAG Core — Document Ingestion + Basic Retrieval  
Phase 3:  Retrieval Excellence — Hybrid Search, Reranking, Optimization
Phase 4:  Memory — Conversation, Entity, and Long-Term Memory Systems
Phase 5:  Tools + Actions — External Integrations, Structured Outputs
Phase 6:  Agents — Single-Agent Reasoning and Planning
Phase 7:  Multi-Agent — Collaboration, Delegation, Specialization
Phase 8:  Evaluation + Observability — Measuring and Monitoring Everything
Phase 9:  Multimodal + Document AI — Vision, Voice, Structured Extraction
Phase 10: Production — Deployment, Scaling, Security, Enterprise Reliability


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