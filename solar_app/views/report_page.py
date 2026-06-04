"""
Step 5 — Report generation page.

Generates a professional PDF report and provides a download button.
"""

from __future__ import annotations

import streamlit as st

from config.translations import get_text
from report.report_generator import generate_report
from views.nav_buttons import render_nav_buttons


def render_report_page(lang: str) -> None:
    """Render the report generation page."""
    st.header(get_text("rpt_title", lang))

    # ── Guard: simulation must be complete ──────────────────────────────
    if st.session_state.simulation_result is None:
        st.warning(get_text("rpt_missing_results", lang))
        render_nav_buttons("report", lang)
        return

    # ── Preview sections ────────────────────────────────────────────────
    result = st.session_state.simulation_result
    config = st.session_state.config
    month_names = get_text("month_names", lang)

    with st.expander(get_text("rpt_exec_summary", lang), expanded=True):
        st.markdown(
            f"- **{get_text('res_annual_yield', lang)}:** {result.annual_yield_kwh:,.0f} kWh\n"
            f"- **{get_text('res_specific_yield', lang)}:** {result.specific_yield_kwh_kwp:,.0f} kWh/kWp\n"
            f"- **{get_text('res_capacity_factor', lang)}:** {result.capacity_factor_pct:.1f}%\n"
            f"- **{get_text('res_performance_ratio', lang)}:** {result.performance_ratio_pct:.1f}%"
        )

    with st.expander(get_text("rpt_monthly_table", lang)):
        import pandas as pd
        monthly_df = pd.DataFrame({
            get_text("res_month", lang): month_names,
            get_text("res_energy_kwh", lang): result.monthly_yield_kwh,
        })
        st.dataframe(monthly_df, use_container_width=True, hide_index=True)

    with st.expander(get_text("rpt_methodology", lang)):
        st.markdown(get_text("rpt_methodology_text", lang))

    with st.expander(get_text("rpt_assumptions", lang)):
        st.markdown(get_text("rpt_assumptions_text", lang))

    # ── Generate PDF ────────────────────────────────────────────────────
    st.markdown("---")
    if st.button(get_text("rpt_generate_btn", lang), type="primary"):
        with st.spinner(get_text("rpt_generating", lang)):
            pdf_bytes = generate_report(
                result=result,
                config=config,
                latitude=st.session_state.latitude,
                longitude=st.session_state.longitude,
                location_name=st.session_state.location_name,
                lang=lang,
            )

        st.download_button(
            label=get_text("rpt_download_btn", lang),
            data=pdf_bytes,
            file_name="solar_pv_report.pdf",
            mime="application/pdf",
        )
        st.success("✅ " + get_text("rpt_download_btn", lang))

    # ── Navigation ──────────────────────────────────────────────────────
    render_nav_buttons("report", lang)
