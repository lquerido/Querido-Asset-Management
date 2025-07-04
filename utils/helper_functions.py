# helper_functions.py
import plotly.express as px
import datetime
import streamlit as st
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetSeries import GetSeries

# helper_functions.py
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetSeries import GetSeries

def build_fund_registry(start, end):        # Todo: Link to config file
    def init_strat(strategy_cls, allocator_cls, tickers, strat_kwargs, alloc_kwargs, weight):
        strat = InitialiseStrategy(
            strategy_cls=strategy_cls,
            allocator_cls=allocator_cls,
            tickers=tickers,
            start=start,
            end=end,
            strategy_kwargs=strat_kwargs,
            allocator_kwargs=alloc_kwargs
        )
        return strat, weight

    # Example volatility data for volatility-scaled allocator
    tickers1 = ["HE=F", "KC=F", "LE=F"]
    tickers2 = ["SGR.AX", "CHN.AX", "TLS.XA"]
    vol_data_1 = GetSeries(ticker=tickers1, start=start, end=end).fetch_volatility()
    vol_data_2 = GetSeries(ticker=tickers2, start=start, end=end).fetch_volatility()

    return {
        "Querido Capital Fund 1": StrategyEnsemble({
            "Momentum": init_strat(
                MomentumStrategy, VolatilityScaledAllocator, tickers1,
                {"lookback": 20, "threshold": 0.02},
                {"vol_data": vol_data_1},
                0.4
            ),
            "Mean Reversion": init_strat(
                MeanReversionStrategy, VolatilityScaledAllocator, tickers2,
                {"lookback": 20, "bound": 1.5},
                {"vol_data": vol_data_2},
                0.6
            ),
        }),
        "Querido Capital Fund 2": StrategyEnsemble({
            "Momentum": init_strat(
                MomentumStrategy, VolatilityScaledAllocator, tickers1,
                {"lookback": 20, "threshold": 0.02},
                {"vol_data": vol_data_1},
                0.8
            ),
            "Mean Reversion": init_strat(
                MeanReversionStrategy, VolatilityScaledAllocator, tickers2,
                {"lookback": 20, "bound": 1.5},
                {"vol_data": vol_data_2},
                0.2
            ),
        }),
        "Querido Capital Fund 3": StrategyEnsemble({
            "Mean Reversion": init_strat(
                MeanReversionStrategy, EqualWeightAllocator, ["AAPL", "MSFT", "TSLA"],
                {"lookback": 20, "bound": 2.0},
                {},
                1.0
            ),
        }),
    }


def render_global_toolbar(fund_registry):
    st.markdown("""
        <style>
            .toolbar {
                position: -webkit-sticky;
                position: sticky;
                top: 0;
                background-color: #f5f2f1;
                padding: 1rem;
                z-index: 999;
                border-bottom: 1px solid #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="toolbar">', unsafe_allow_html=True)

    fund_list = list(fund_registry.keys())

    # First row: Fund & Strategy
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Fund", fund_list, key="fund")
    selected_fund = st.session_state.get("fund", fund_list[0])
    strategy_list = list(fund_registry[selected_fund].capital_allocation.keys())
    with col2:
        st.selectbox("Strategy", strategy_list, key="strategy")

    # Second row: Start & End Date
    col3, col4 = st.columns(2)
    with col3:
        st.date_input("Start Date", value=datetime.date(2020, 1, 1), key="start_date")
    with col4:
        st.date_input("End Date", value=datetime.date.today(), key="end_date")

    st.markdown('</div>', unsafe_allow_html=True)


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

def render_dual_line_chart(title, series):
    fig = px.line(x=series.index, y=series.values, labels={"x": "Date", "y": title})
    fig.update_traces(line=dict(color="#207f73", width=3))
    fig.update_layout(
        height=350,
        margin=dict(t=20, b=20),
        xaxis=dict(title="Date"),
        yaxis=dict(title=title),
        plot_bgcolor="#f5f2f1",
        paper_bgcolor="#f5f2f1",
        font=dict(color="#1a1a1a")
    )
    st.plotly_chart(fig, use_container_width=True)


def render_stacked_bar_chart(title, categories, values, x_title="", y_title=""):
    fig = px.bar(x=categories, y=values, labels={"x": x_title, "y": y_title})
    fig.update_layout(
        title=title,
        barmode='stack',
        xaxis_title=x_title,
        yaxis_title=y_title,
        plot_bgcolor="#f5f2f1",
        paper_bgcolor="#f5f2f1",
        font=dict(color="#1a1a1a"),
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_green_line_chart(title, series_list, labels):
    import plotly.graph_objects as go

    colors = ["#207f73", "#94c9ad"]  # Two shades of green (you can add more if needed)

    fig = go.Figure()
    for i, (s, label) in enumerate(zip(series_list, labels)):
        fig.add_trace(go.Scatter(
            x=s.index,
            y=s.values,
            mode='lines',
            name=label,
            line=dict(color=colors[i % len(colors)], width=3)
        ))

    fig.update_layout(
        title=title,
        plot_bgcolor="#f5f2f1",
        paper_bgcolor="#f5f2f1",
        font=dict(color="#1a1a1a"),
        height=400,
        margin=dict(t=30, b=30),
        xaxis_title="Date",
        yaxis_title=title
    )
    st.plotly_chart(fig, use_container_width=True)


def render_green_bar_chart(title, values, labels):
    fig = px.bar(x=labels, y=values, labels={"x": "Date", "y": title})
    fig.update_traces(marker_color="#207f73")
    fig.update_layout(
        height=350,
        margin=dict(t=20, b=20),
        plot_bgcolor="#f5f2f1",
        paper_bgcolor="#f5f2f1",
        font=dict(color="#1a1a1a"),
        xaxis_title="Date",
        yaxis_title=title
    )
    st.plotly_chart(fig, use_container_width=True)


def render_drawdown_chart(title, drawdown_series):
    fig = px.area(x=drawdown_series.index, y=drawdown_series.values)
    fig.update_traces(line_color="#207f73")
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Drawdown",
        height=350,
        margin=dict(t=20, b=20),
        yaxis=dict(tickformat=".0%")
    )
    st.plotly_chart(fig, use_container_width=True)