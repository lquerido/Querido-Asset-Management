# helper_functions.py
import streamlit as st
import plotly.express as px

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


def render_markdown_from_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    st.markdown(content, unsafe_allow_html=True)  # Use unsafe_html if you're adding custom HTML


def render_styled_bar_chart(title, labels, values, x_title="", y_title=""):
    st.markdown(f"**{title}**")
    fig = px.bar(x=labels, y=values, labels={"x": x_title, "y": y_title})

    fig.update_traces(marker_color="#207f73")  # ✅ Set bars to green

    fig.update_layout(
        margin=dict(t=20, b=20),
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
    )
    st.plotly_chart(fig, use_container_width=True)

def render_styled_pie_chart(title, labels, values):
    st.markdown(f"**{title}**")

    # A range of green/teal hues
    color_palette = ["#1a7f5a", "#2ecc71", "#27ae60", "#16a085", "#1abc9c"]

    fig = px.pie(
        names=labels,
        values=values,
        color_discrete_sequence=color_palette[:len(labels)]  # auto-truncate to needed length
    )
    fig.update_layout(
        margin=dict(t=20, b=20),
        font=dict(color="white"),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

def render_styled_brinson_table(df, index_col="Sector"):
    st.markdown("### Brinson Attribution")
    st.write("Allocation vs. Selection Effect at Sector level")

    styled_df = df.set_index(index_col).style.background_gradient(
        axis=0,
        cmap="Greens"  # ✅ Green-themed heatmap
    )

    st.dataframe(styled_df)