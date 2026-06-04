"""
Solar PV Yield Calculator — Streamlit application entry point.

Manages page navigation, language selection, session state
initialisation, and the sidebar configuration summary.
"""

from __future__ import annotations

import streamlit as st

from config.translations import get_text

# ---------------------------------------------------------------------------
# Page config (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Solar PV Yield Calculator",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Session-state defaults
# ---------------------------------------------------------------------------
_DEFAULTS = {
    "lang": "en",
    "latitude": None,
    "longitude": None,
    "location_name": "",
    "weather_data": None,
    "config": None,
    "config_mode": "quick",
    "simulation_result": None,
    "current_page": "location",
}

for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------------------------------------------------------------------
# Language selector (sidebar top)
# ---------------------------------------------------------------------------
lang_options = {"English": "en", "Deutsch": "de"}
selected_lang_label = st.sidebar.selectbox(
    get_text("language_label", st.session_state.lang),
    options=list(lang_options.keys()),
    index=0 if st.session_state.lang == "en" else 1,
)
st.session_state.lang = lang_options[selected_lang_label]
lang = st.session_state.lang

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
PAGES = {
    "location": get_text("nav_location", lang),
    "weather": get_text("nav_weather", lang),
    "system_config": get_text("nav_system", lang),
    "results": get_text("nav_results", lang),
    "report": get_text("nav_report", lang),
}

st.sidebar.markdown("---")
selected_page = st.sidebar.radio(
    "Navigation",
    options=list(PAGES.keys()),
    format_func=lambda k: PAGES[k],
    index=list(PAGES.keys()).index(st.session_state.current_page),
    label_visibility="collapsed",
)
st.session_state.current_page = selected_page

# ---------------------------------------------------------------------------
# Sidebar — configuration summary
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {get_text('sidebar_title', lang)}")

if st.session_state.latitude is not None:
    st.sidebar.markdown(
        f"**{get_text('sidebar_lat', lang)}:** {st.session_state.latitude:.4f}°  \n"
        f"**{get_text('sidebar_lon', lang)}:** {st.session_state.longitude:.4f}°"
    )
    if st.session_state.location_name:
        st.sidebar.caption(st.session_state.location_name)
else:
    st.sidebar.caption(f"{get_text('sidebar_location', lang)}: —")

weather_status = (
    get_text("sidebar_loaded", lang)
    if st.session_state.weather_data is not None
    else get_text("sidebar_not_loaded", lang)
)
st.sidebar.markdown(f"**{get_text('sidebar_weather_status', lang)}:** {weather_status}")

if st.session_state.config is not None:
    cfg = st.session_state.config
    st.sidebar.markdown(
        f"**{get_text('sidebar_mode', lang)}:** {st.session_state.config_mode.title()}  \n"
        f"**{get_text('sidebar_kwp', lang)}:** {cfg.kwp}  \n"
        f"**{get_text('sidebar_tilt', lang)}:** {cfg.tilt_deg}°  \n"
        f"**{get_text('sidebar_azimuth', lang)}:** {cfg.azimuth_deg}°"
    )

# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
if selected_page == "location":
    from views.location import render_location_page
    render_location_page(lang)

elif selected_page == "weather":
    from views.weather import render_weather_page
    render_weather_page(lang)

elif selected_page == "system_config":
    from views.system_config import render_system_config_page
    render_system_config_page(lang)

elif selected_page == "results":
    from views.results import render_results_page
    render_results_page(lang)

elif selected_page == "report":
    from views.report_page import render_report_page
    render_report_page(lang)
