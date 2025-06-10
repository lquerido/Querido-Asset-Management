import streamlit as st
import os

RESEARCH_DIR = "views/subview_utils/investment_research"  # Directory where markdown files live


def render(subview):
    st.title("Investment Research")

    if subview == "Macro" or subview == "Equities":
        # List all markdown files
        if not os.path.exists(RESEARCH_DIR):
            st.warning("No research papers found.")
            return

        papers = [f for f in os.listdir(RESEARCH_DIR) if f.endswith(".md")]

        if not papers:
            st.info("No papers available yet.")
            return

        selected_paper = st.selectbox("Select a research paper:", papers)

        with open(os.path.join(RESEARCH_DIR, selected_paper), "r") as f:
            content = f.read()
            st.markdown(content)

        # Optional download as PDF (stub for now)
        st.download_button(
            label="Download PDF",
            data=b"PDF generation placeholder.",
            file_name=selected_paper.replace(".md", ".pdf"),
            mime="application/pdf"
        )
