"""
HesabuAgent tools — COB data loader and OCDS query client.
"""
import os
import httpx
import pandas as pd
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).parent.parent / "civic_data"

class COBDataInput(BaseModel):
    county: str = Field(description="Kenya county name e.g. Turkana, Nairobi")

class COBDataTool(BaseTool):
    name: str = "cob_budget_data"
    description: str = (
        "Query Controller of Budget county budget execution data for FY 2022/23. "
        "Returns allocation, absorption rate, and sector breakdown for the specified county."
    )
    args_schema: type[BaseModel] = COBDataInput

    def _run(self, county: str) -> str:
        fpath = DATA_DIR / "county_budgets_fy2223.csv"
        if not fpath.exists():
            return "COB data not found. Place county_budgets_fy2223.csv in civic_data/"
        df = pd.read_csv(fpath)
        # Case-insensitive county match
        mask = df.apply(lambda col: col.astype(str).str.lower()).apply(
            lambda row: county.lower() in " ".join(row), axis=1
        )
        matches = df[mask]
        if matches.empty:
            return f"No COB data found for county: {county}"
        return matches.to_string(index=False)

class OCDSQueryInput(BaseModel):
    county: str = Field(description="Kenya county name")
    year: int = Field(default=2023, description="Year to query OCDS data for")

class OCDSQueryTool(BaseTool):
    name: str = "ocds_procurement_data"
    description: str = (
        "Query Kenya OCDS procurement contracts from tenders.go.ke/ocds. "
        "Returns contract awards and tender notices for the specified county."
    )
    args_schema: type[BaseModel] = OCDSQueryInput

    def _run(self, county: str, year: int = 2023) -> str:
        sandbox = os.getenv("SANDBOX", "true").lower() == "true"
        if sandbox:
            return (
                f"SANDBOX MODE: OCDS data for {county} ({year})\n"
                f"Contracts found: 8 | Awarded: 5 | Total value: KES 320M\n"
                f"Source: tenders.go.ke/ocds (sandbox simulation)\n"
                f"Set SANDBOX=false for live OCDS data."
            )
        try:
            r = httpx.get(
                "https://tenders.go.ke/ocds/packages",
                params={"publisher": county.lower(), "year": year},
                timeout=15
            )
            return r.text[:2000]  # truncate for agent context window
        except Exception as e:
            return f"OCDS query failed: {str(e)}"
