"""
Step 4 — Simulation results page.

Runs the pvlib simulation, displays KPI cards, a monthly production
bar chart, and provides CSV download.
"""

from __future__ import annotations

import io

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config.translations import get_text
from models.pv_model import run_simulation
from views.nav_buttons import render_nav_buttons


def render_results_page(lang: str) -> None:
    """Render the simulation results page."""
    st.header(get_text("res_title", lang))

    # ── Guard: prerequisites ────────────────────────────────────────────
    if (
        st.session_state.latitude is None
        or st.session_state.weather_data is None
        or st.session_state.config is None
    ):
        st.warning(get_text("res_missing_config", lang))
        render_nav_buttons("results", lang)
        return

    # ── Run simulation ──────────────────────────────────────────────────
    if st.button(get_text("res_run_btn", lang), type="primary"):
        with st.spinner(get_text("res_running", lang)):
            result = run_simulation(
                weather_df=st.session_state.weather_data,
                latitude=st.session_state.latitude,
                longitude=st.session_state.longitude,
                config=st.session_state.config,
            )
            st.session_state.simulation_result = result

    result = st.session_state.simulation_result
    if result is None:
        st.info(get_text("res_run_btn", lang))
        return

    # ── KPI cards ───────────────────────────────────────────────────────
    st.markdown("---")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            get_text("res_annual_yield", lang),
            f"{result.annual_yield_kwh:,.0f}",
        )
    with kpi2:
        st.metric(
            get_text("res_specific_yield", lang),
            f"{result.specific_yield_kwh_kwp:,.0f}",
        )
    with kpi3:
        st.metric(
            get_text("res_capacity_factor", lang),
            f"{result.capacity_factor_pct:.1f}%",
        )
    with kpi4:
        st.metric(
            get_text("res_performance_ratio", lang),
            f"{result.performance_ratio_pct:.1f}%",
        )

    # ── Monthly bar chart ───────────────────────────────────────────────
    st.markdown("---")
    month_names = get_text("month_names", lang)
    fig = go.Figure(
        data=[
            go.Bar(
                x=month_names,
                y=result.monthly_yield_kwh,
                marker_color="#FF8F00",
                text=[f"{v:,.0f}" for v in result.monthly_yield_kwh],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        title=get_text("res_monthly_chart_title", lang),
        xaxis_title=get_text("res_month", lang),
        yaxis_title=get_text("res_energy_kwh", lang),
        height=420,
        margin=dict(t=60, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(gridcolor="rgba(200,200,200,0.3)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Monthly table ───────────────────────────────────────────────────
    monthly_df = pd.DataFrame({
        get_text("res_month", lang): month_names,
        get_text("res_energy_kwh", lang): [f"{v:,.1f}" for v in result.monthly_yield_kwh],
    })
    monthly_df = monthly_df.set_index(get_text("res_month", lang))
    st.table(monthly_df)

    # ── CSV download ────────────────────────────────────────────────────
    st.markdown("---")
    if result.hourly_ac_power_w is not None:
        weather_df = st.session_state.weather_data
        csv_df = pd.DataFrame({
            "timestamp_utc": weather_df.index[:len(result.hourly_ac_power_w)],
            "ac_power_w": result.hourly_ac_power_w,
        })
        csv_buffer = io.StringIO()
        csv_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label=get_text("res_download_csv", lang),
            data=csv_buffer.getvalue(),
            file_name="pv_simulation_results.csv",
            mime="text/csv",
        )

    # ── Navigation ──────────────────────────────────────────────────────
    render_nav_buttons("results", lang)
