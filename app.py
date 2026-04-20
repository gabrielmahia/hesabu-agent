"""
HesabuAgent — Streamlit interface for county budget analysis crew.
"""
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="HesabuAgent", page_icon="💰", layout="centered")
st.title("💰 HesabuAgent")
st.caption("Kenya county budget intelligence — powered by CrewAI + OCDS data")

COUNTIES = [
    "Nairobi","Mombasa","Kiambu","Nakuru","Machakos","Kisumu","Meru","Kakamega",
    "Bungoma","Kilifi","Turkana","Garissa","Wajir","Mandera","Marsabit","Isiolo",
]

with st.form("run_crew"):
    county  = st.selectbox("Select county:", COUNTIES)
    llm_key = st.text_input("Anthropic API key:", type="password",
                             value=os.getenv("ANTHROPIC_API_KEY",""))
    sandbox = st.checkbox("Sandbox mode (no live API calls)", value=True)
    submit  = st.form_submit_button("Analyse county budget", type="primary")

if submit:
    if not llm_key:
        st.error("Provide an Anthropic API key to run the crew.")
        st.stop()
    os.environ["ANTHROPIC_API_KEY"] = llm_key
    os.environ["SANDBOX"] = "true" if sandbox else "false"

    with st.spinner(f"Running HesabuAgent crew for {county}..."):
        try:
            from crewai import Crew, Task
            from crew.agents import build_crew_agents

            budget_analyst, procurement_analyst, report_writer = build_crew_agents()

            t1 = Task(
                description=f"Retrieve and summarise Controller of Budget execution data for {county} county, FY 2022/23.",
                expected_output="County name, total development allocation (KES), amount absorbed (KES), absorption rate (%), sector breakdown.",
                agent=budget_analyst,
            )
            t2 = Task(
                description=f"Query OCDS procurement contracts for {county} county for 2022/23. List awarded contracts and total value.",
                expected_output="Number of contracts, total awarded value (KES), key procurement categories.",
                agent=procurement_analyst,
            )
            t3 = Task(
                description=f"Write a 300-word accountability brief for {county} county combining budget absorption and procurement findings. Flag any gaps between budget spend and procurement records.",
                expected_output="Plain-language brief with: budget summary, procurement summary, identified gaps, recommended next steps for oversight.",
                agent=report_writer,
                context=[t1, t2],
            )
            crew = Crew(agents=[budget_analyst, procurement_analyst, report_writer], tasks=[t1, t2, t3], verbose=False)
            result = crew.kickoff()
            st.markdown("### County Accountability Brief")
            st.write(str(result))
        except ImportError:
            st.error("CrewAI not installed. Run: pip install crewai")
        except Exception as e:
            st.error(f"Crew run failed: {e}")

st.divider()
st.caption("Data: Controller of Budget · OCDS Kenya (tenders.go.ke/ocds) · © 2026 Gabriel Mahia")
