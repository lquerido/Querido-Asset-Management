import streamlit as st
import os

RESEARCH_DIR = "views/subview_utils/investment_research"   # Directory where markdown files live
PDF_DIR = "views/subview_utils/investment_research/pdfs"         # Matching PDFs
LATEX_DIR = "views/subview_utils/investment_research/latex"      # Matching LaTeX files

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

        base_filename = selected_paper.replace(".md", "")

        # PDF Download
        pdf_path = os.path.join(PDF_DIR, f"{base_filename}.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=f"{base_filename}.pdf",
                    mime="application/pdf"
                )

        # LaTeX Source Download
        tex_path = os.path.join(LATEX_DIR, f"{base_filename}.tex")
        if os.path.exists(tex_path):
            with open(tex_path, "rb") as f:
                st.download_button(
                    label="Download LaTeX",
                    data=f,
                    file_name=f"{base_filename}.tex",
                    mime="application/x-tex"
                )
