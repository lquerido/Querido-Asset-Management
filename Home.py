import streamlit as st
from utils.helper_functions import render_markdown_from_file

st.set_page_config(layout="wide")

# --- Two Columns Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("<h1 style='text-align: left;'>Querido Capital Management</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **Querido Capital Management** platform. **Querido Capital Management** is a data-driven investment research and portfolio management firm. Our focus is on idea generation, investment research and strategy development.
    
    To navigate the platform, use the left sidebar.
    
    _Please reach out if you'd be interested in collaborating on research or would just like to connect!_
    [Check out my GitHub](https://github.com/lquerido/Querido-Asset-Management) or 
    [connect on LinkedIn](https://linkedin.com/in/liam-querido-aiaa-1235281b7/).
    """)

with col2:
    st.image("static/liam_querido.jpg")

st.markdown("---")

render_markdown_from_file("pages/subview_utils/about_us/about.md")