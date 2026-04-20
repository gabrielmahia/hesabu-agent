"""
HesabuAgent — CrewAI agents for Kenya budget analysis.
"""
from crewai import Agent
from .tools import COBDataTool, OCDSQueryTool

def build_crew_agents(llm=None):
    """Build the three-agent crew for Kenya budget analysis."""

    budget_analyst = Agent(
        role="Kenya County Budget Analyst",
        goal=(
            "Analyse county budget execution data from the Controller of Budget. "
            "Identify absorption rates, unspent balances, and spending patterns for the target county."
        ),
        backstory=(
            "You are a public finance specialist who has studied all 47 Kenya county governments. "
            "You read COB quarterly reports fluently and can calculate absorption rates, "
            "flag anomalies, and contextualise spending within devolution policy."
        ),
        tools=[COBDataTool()],
        verbose=True,
        llm=llm,
        allow_delegation=False,
    )

    procurement_analyst = Agent(
        role="Kenya Procurement Analyst",
        goal=(
            "Query OCDS procurement contracts for the target county. "
            "Map awarded contracts to budget line items and flag gaps."
        ),
        backstory=(
            "You specialise in the Open Contracting Data Standard (OCDS) and know Kenya's "
            "Public Procurement and Asset Disposal Act. You query tenders.go.ke/ocds and "
            "can identify when budget absorption lacks procurement paper trails."
        ),
        tools=[OCDSQueryTool()],
        verbose=True,
        llm=llm,
        allow_delegation=False,
    )

    report_writer = Agent(
        role="Accountability Report Writer",
        goal=(
            "Synthesise findings from the Budget Analyst and Procurement Analyst into a "
            "plain-language county accountability brief suitable for civil society, journalists, "
            "and county assembly members."
        ),
        backstory=(
            "You write for two audiences: the technically literate (county assembly members, NGOs) "
            "and the general public. You translate KES figures and absorption percentages into "
            "plain narratives, always citing sources and noting limitations."
        ),
        tools=[],
        verbose=True,
        llm=llm,
        allow_delegation=False,
    )

    return budget_analyst, procurement_analyst, report_writer
