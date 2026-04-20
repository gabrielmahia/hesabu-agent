# AGENTS.md — HesabuAgent

## Purpose
CrewAI multi-agent system correlating COB county budget data with OCDS procurement contracts.

## Agents
- Budget Analyst — reads COB CSVs, calculates absorption rates
- Procurement Analyst — queries tenders.go.ke/ocds (SANDBOX=true for testing)
- Report Writer — synthesises into plain-language briefs

## Key rules
- Never fabricate procurement figures
- Always cite data sources in output
- SANDBOX=true is default — live OCDS requires SANDBOX=false
- COB data files go in civic_data/ (not in version control — see .gitignore)
