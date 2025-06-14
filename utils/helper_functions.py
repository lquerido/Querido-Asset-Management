# helper_functions.py

import streamlit as st

def render_metric_grid(metrics: list[tuple[str, str]], columns: int = 3):
    for i in range(0, len(metrics), columns):
        if i > 0:
            st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        cols = st.columns(columns)
        for col, (label, value) in zip(cols, metrics[i:i + columns]):
            col.markdown(f"""
                <div style="
                    background-color: #207f73;
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: left;
                ">
                    <div style="font-size: 0.9rem; color: #ffffff; font-family: sans-serif;">{label}</div>
                    <div style="border-top: 1px solid #ffffff; margin: 0.5rem 0;"></div>
                    <div style="font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 600; color: #ffffff; text-align: center;">
                        {value}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
