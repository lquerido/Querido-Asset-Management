import streamlit as st

def render_markdown_from_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    st.markdown(content, unsafe_allow_html=True)  # Use unsafe_html if you're adding custom HTML

def render(subview):
    st.title("About Querido Capital Management")

    if subview == "About":
        render_markdown_from_file("views/subview_utils/about_us/about.md")
    elif subview == "Our Strategies":
        render_markdown_from_file("views/subview_utils/about_us/our_strategies.md")
    elif subview == "Dashboard Logic":
        render_markdown_from_file("views/subview_utils/about_us/dashboard_logic.md")

