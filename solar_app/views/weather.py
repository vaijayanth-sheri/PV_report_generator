"""
Step 2 — Weather data retrieval page.

Fetches PVGIS TMY data for the confirmed location, displays summary
statistics and an irradiance preview chart.
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.translations import get_text
from services.pvgis_client import fetch_tmy_data, PVGISError
from views.nav_buttons import render_nav_buttons


def render_weather_page(lang: str) -> None:
    """Render the weather data retrieval page."""
    st.header(get_text("weather_title", lang))

    # ── Guard: location must be set ─────────────────────────────────────
    if st.session_state.latitude is None or st.session_state.longitude is None:
        st.warning(get_text("weather_location_missing", lang))
        render_nav_buttons("weather", lang)
        return

    lat = st.session_state.latitude
    lon = st.session_state.longitude

    st.markdown(f"📍 **{get_text('sidebar_lat', lang)}:** {lat:.4f}° | "
                f"**{get_text('sidebar_lon', lang)}:** {lon:.4f}°")

    # ── Fetch button ────────────────────────────────────────────────────
    if st.button(get_text("weather_fetch_btn", lang), type="primary"):
        with st.spinner(get_text("weather_fetching", lang)):
            try:
                df = fetch_tmy_data(lat, lon)
                st.session_state.weather_data = df
                st.success(get_text("weather_success", lang, rows=len(df)))
            except PVGISError as exc:
                st.error(get_text("weather_fail", lang, error=str(exc)))
                return

    # ── Display loaded data ─────────────────────────────────────────────
    df = st.session_state.weather_data
    if df is None:
        st.info(get_text("weather_fetch_btn", lang))
        return

    # Summary statistics
    st.subheader(get_text("weather_stats", lang))
    display_cols = ["ghi", "dni", "dhi", "temp_air", "wind_speed"]
    available_cols = [c for c in display_cols if c in df.columns]
    col_labels = {
        "ghi": get_text("weather_ghi", lang),
        "dni": get_text("weather_dni", lang),
        "dhi": get_text("weather_dhi", lang),
        "temp_air": get_text("weather_temp", lang),
        "wind_speed": get_text("weather_wind", lang),
    }

    stats = df[available_cols].describe().T
    stats.index = [col_labels.get(c, c) for c in stats.index]
    st.dataframe(stats.style.format("{:.1f}"), use_container_width=True)

    # ── Irradiance chart ────────────────────────────────────────────────
    st.subheader(get_text("weather_preview", lang))
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(
            get_text("weather_ghi", lang),
            get_text("weather_temp", lang),
        ),
    )

    # Monthly means for a cleaner chart
    monthly_ghi = df["ghi"].resample("ME").mean() if "ghi" in df.columns else None
    monthly_temp = df["temp_air"].resample("ME").mean() if "temp_air" in df.columns else None

    if monthly_ghi is not None:
        fig.add_trace(
            go.Bar(
                x=monthly_ghi.index.strftime("%b"),
                y=monthly_ghi.values,
                name="GHI",
                marker_color="#FFA726",
            ),
            row=1, col=1,
        )

    if monthly_temp is not None:
        fig.add_trace(
            go.Bar(
                x=monthly_temp.index.strftime("%b"),
                y=monthly_temp.values,
                name="Temp",
                marker_color="#42A5F5",
            ),
            row=2, col=1,
        )

    fig.update_layout(height=450, showlegend=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # ── Data preview table ──────────────────────────────────────────────
    with st.expander(get_text("weather_preview", lang)):
        st.dataframe(df.head(48), use_container_width=True)

    # ── Navigation ──────────────────────────────────────────────────────
    render_nav_buttons("weather", lang)
