# 💰 HesabuAgent — Kenya Budget Intelligence Agent

> Multi-agent AI system for analysing Kenya county budget execution. Built on [CrewAI](https://github.com/crewaiinc/crewai) — correlates Controller of Budget absorption data with OCDS procurement contracts.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Built on CrewAI](https://img.shields.io/badge/Built%20on-CrewAI-orange)](https://crewai.com)

## What it does

HesabuAgent deploys a crew of specialised AI agents to answer the hardest question in Kenya's devolution accountability:

> *"County X was allocated KES 800M for development. It absorbed only 62%. Where did the money go — and what did it procure?"*

**Three agents, one crew:**

| Agent | Role | Data source |
|-------|------|-------------|
| **Budget Analyst** | Reads COB absorption rates, flags low-performing counties | `county_budgets_fy2223.csv` |
| **Procurement Analyst** | Queries OCDS tenders from `tenders.go.ke/ocds` | OCDS API |
| **Report Writer** | Synthesises findings into plain-language county brief | Both |

## Sample output

```
County: Turkana
Development budget: KES 4.2B
Absorbed: 41% (KES 1.72B)
Unspent: KES 2.48B

Procurement contracts (OCDS):
  - 12 tenders published, 8 awarded
  - KES 890M in awarded contracts — roads and water infrastructure
  - KES 830M gap: no matching procurement records

Assessment: KES 830M in development spend has no procurement paper trail.
Recommend: County Assembly to request statement of account under PFM Act.
```

## Quickstart

```bash
pip install hesabu-agent
# or from source:
git clone https://github.com/gabrielmahia/hesabu-agent
cd hesabu-agent
pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key
streamlit run app.py
```

## Architecture

```
crew/
  ├── agents.py      ← Budget Analyst, Procurement Analyst, Report Writer
  ├── tasks.py       ← Task definitions for each agent
  └── tools.py       ← COB data loader, OCDS API client, CSV tools
app.py               ← Streamlit interface
```

Built on [CrewAI](https://github.com/crewaiinc/crewai) (49k+ GitHub stars, MIT) — the leading multi-agent orchestration framework for Python.

## Data sources

- **Controller of Budget** — county budget execution reports (our published dataset: [Kaggle DOI](https://doi.org/10.34740/kaggle/dsv/15473045) / [HuggingFace DOI](https://doi.org/10.57967/hf/8223))
- **OCDS Kenya** — procurement data via [tenders.go.ke/ocds](https://tenders.go.ke/ocds) (confirmed by Open Contracting Partnership — see [open-contracting/standard#1745](https://github.com/open-contracting/standard/issues/1745))

## Why CrewAI

CrewAI's role-based agent model matches how budget accountability actually works — different people examine different data slices and then synthesise findings. Each agent has a clear mandate, preventing hallucination through role-constrained prompting.

## Related

- [Hesabu](https://hesabu.streamlit.app) — The Streamlit dashboard version
- [kenya-rag](https://github.com/gabrielmahia/kenya-rag) — RAG over Kenya civic datasets
- [mpesa-mcp](https://pypi.org/project/mpesa-mcp/) — M-Pesa MCP server

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: CC BY-NC-ND 4.0
Data: OCDS Kenya (Open Contracting Partnership), Controller of Budget Kenya.
Not affiliated with any county government or the Controller of Budget.
