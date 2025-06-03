import streamlit as st

def render(subview):
    st.title("Detailed Investment Performance Analysis")

    if subview == "Trade-by-Trade Analysis":
        st.write("Placeholder: trade-by-trade breakdown")
    elif subview == "Time-Weighted Returns":
        st.write("Placeholder: cumulative return vs benchmark")
    elif subview == "Portfolio Composition":
        st.write("Placeholder: current weights")
    elif subview == "Portfolio Risk":
        st.write("Placeholder: risk metrics")
    elif subview == "Performance Factors":
        st.write("Placeholder: turnover, win/loss ratio, etc.")
