import streamlit as st

st.markdown("<h2 style='text-align: center;'>Investment Research</h2>", unsafe_allow_html=True)

# --- Sample Research Papers ---
research_papers = [
    {
        "title": "Momentum in Global Equity Markets",
        "read_time": "8 min read",
        "summary": "A practical overview of cross-sectional momentum strategies across regions.",
        "easy_file": "files/momentum_easy.pdf",
        "latex_file": "files/momentum_academic.pdf"
    },
    {
        "title": "Value Investing in the Modern Era",
        "read_time": "10 min read",
        "summary": "Revisiting value factors in the presence of intangible assets and macro trends.",
        "easy_file": "files/value_easy.pdf",
        "latex_file": "files/value_academic.pdf"
    },
    {
        "title": "Macro Risk Premia Explained",
        "read_time": "12 min read",
        "summary": "An overview of macro risk premia and how they influence multi-asset portfolios.",
        "easy_file": "files/macro_easy.pdf",
        "latex_file": "files/macro_academic.pdf"
    }
]

# --- Layout ---
for paper in research_papers:
    with st.container():
        st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            ">
                <h4 style="margin-bottom:0;">{paper['title']}</h4>
                <p style="margin-top:0.2rem; color: #666;">{paper['read_time']}</p>
                <p>{paper['summary']}</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📘 Easy Version", data="Fake PDF content", file_name=paper["easy_file"], mime="application/pdf")
        with col2:
            st.download_button("📄 Academic Version", data="Fake PDF content", file_name=paper["latex_file"], mime="application/pdf")

        st.markdown("---")
