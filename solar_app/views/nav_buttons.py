"""
Shared navigation helpers for Streamlit pages.

Provides Next/Back buttons that save state and navigate between
the 5-step workflow.
"""

from __future__ import annotations

import streamlit as st

from config.translations import get_text

# Ordered page keys for the workflow
PAGE_ORDER = ["location", "weather", "system_config", "results", "report"]


def render_nav_buttons(current_page: str, lang: str) -> None:
    """Render Back / Next navigation buttons at the bottom of a page.

    Parameters
    ----------
    current_page : str
        Key of the current page (e.g. "location").
    lang : str
        Active language code.
    """
    idx = PAGE_ORDER.index(current_page)
    has_back = idx > 0
    has_next = idx < len(PAGE_ORDER) - 1

    st.markdown("---")
    cols = st.columns([1, 6, 1])

    with cols[0]:
        if has_back:
            if st.button(f"← {get_text('nav_back', lang)}", use_container_width=True):
                st.session_state.current_page = PAGE_ORDER[idx - 1]
                st.rerun()

    with cols[2]:
        if has_next:
            if st.button(f"{get_text('nav_next', lang)} →", type="primary", use_container_width=True):
                st.session_state.current_page = PAGE_ORDER[idx + 1]
                st.rerun()
