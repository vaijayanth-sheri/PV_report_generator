"""
Step 3 — System configuration page.

Provides Quick Mode and Pro Mode configuration forms.
"""

from __future__ import annotations

import streamlit as st

from config.translations import get_text
from models.assumptions import (
    DetailedLosses,
    MODULE_TYPES,
    ProConfig,
    QuickConfig,
)
from services.validation import validate_system_config, validate_pro_config
from views.nav_buttons import render_nav_buttons


def render_system_config_page(lang: str) -> None:
    """Render the system configuration page."""
    st.header(get_text("sys_title", lang))

    # ── Mode selection ──────────────────────────────────────────────────
    mode = st.radio(
        get_text("sidebar_mode", lang),
        options=["quick", "pro"],
        format_func=lambda m: get_text(f"sys_mode_{m}", lang),
        horizontal=True,
        index=0 if st.session_state.config_mode == "quick" else 1,
    )
    st.session_state.config_mode = mode

    st.markdown("---")

    # ── Common parameters ───────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        kwp = st.number_input(
            get_text("sys_kwp", lang),
            min_value=0.1, max_value=100000.0, value=5.0, step=0.5,
            format="%.1f",
        )
        tilt = st.number_input(
            get_text("sys_tilt", lang),
            min_value=0.0, max_value=90.0, value=30.0, step=1.0,
            format="%.1f",
        )

    with col2:
        azimuth = st.number_input(
            get_text("sys_azimuth", lang),
            min_value=0.0, max_value=360.0, value=180.0, step=1.0,
            format="%.1f",
            help="0°=N, 90°=E, 180°=S, 270°=W",
        )
        inv_eff = st.number_input(
            get_text("sys_inv_eff", lang),
            min_value=80.0, max_value=100.0, value=96.0, step=0.5,
            format="%.1f",
        )

    # ── Quick Mode ──────────────────────────────────────────────────────
    if mode == "quick":
        losses = st.slider(
            get_text("sys_losses", lang),
            min_value=0.0, max_value=50.0, value=14.0, step=0.5,
        )

        if st.button(get_text("sys_confirm_btn", lang), type="primary"):
            errors = validate_system_config(kwp, tilt, azimuth, losses, inv_eff)
            if errors:
                for e in errors:
                    st.error(get_text(e, lang))
            else:
                st.session_state.config = QuickConfig(
                    kwp=kwp,
                    tilt_deg=tilt,
                    azimuth_deg=azimuth,
                    system_losses_pct=losses,
                    inverter_efficiency_pct=inv_eff,
                )
                st.success(get_text("sys_saved", lang))

    # ── Pro Mode ────────────────────────────────────────────────────────
    else:
        st.subheader(get_text("sys_mode_pro", lang))

        col_a, col_b = st.columns(2)
        with col_a:
            dc_ac_ratio = st.number_input(
                get_text("sys_dc_ac", lang),
                min_value=0.5, max_value=3.0, value=1.2, step=0.05,
                format="%.2f",
            )
            albedo = st.number_input(
                get_text("sys_albedo", lang),
                min_value=0.0, max_value=1.0, value=0.2, step=0.05,
                format="%.2f",
            )

        with col_b:
            transposition_options = ["perez", "isotropic", "haydavies", "klucher"]
            transposition = st.selectbox(
                get_text("sys_transposition", lang),
                options=transposition_options,
                index=0,
            )

            module_keys = list(MODULE_TYPES.keys())
            module_labels = [
                MODULE_TYPES[k][f"description_{lang}"]
                if f"description_{lang}" in MODULE_TYPES[k]
                else MODULE_TYPES[k]["description_en"]
                for k in module_keys
            ]
            module_idx = st.selectbox(
                get_text("sys_module_type", lang),
                options=range(len(module_keys)),
                format_func=lambda i: module_labels[i],
                index=0,
            )
            selected_module = module_keys[module_idx]

        # ── Detailed losses ─────────────────────────────────────────────
        st.markdown("#### " + get_text("sys_losses", lang))
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            l_soiling = st.number_input(get_text("sys_losses_soiling", lang), 0.0, 20.0, 2.0, 0.5)
            l_shading = st.number_input(get_text("sys_losses_shading", lang), 0.0, 30.0, 3.0, 0.5)
        with lc2:
            l_mismatch = st.number_input(get_text("sys_losses_mismatch", lang), 0.0, 10.0, 2.0, 0.5)
            l_wiring = st.number_input(get_text("sys_losses_wiring", lang), 0.0, 10.0, 2.0, 0.5)
        with lc3:
            l_aging = st.number_input(get_text("sys_losses_aging", lang), 0.0, 10.0, 1.5, 0.5)

        if st.button(get_text("sys_confirm_btn", lang), type="primary"):
            errors = validate_system_config(kwp, tilt, azimuth, 0.0, inv_eff)
            errors += validate_pro_config(dc_ac_ratio, albedo)
            if errors:
                for e in errors:
                    st.error(get_text(e, lang) if not e[0].isupper() else e)
            else:
                detailed = DetailedLosses(
                    soiling_pct=l_soiling,
                    shading_pct=l_shading,
                    mismatch_pct=l_mismatch,
                    wiring_dc_pct=l_wiring,
                    aging_pct=l_aging,
                )
                st.session_state.config = ProConfig(
                    kwp=kwp,
                    tilt_deg=tilt,
                    azimuth_deg=azimuth,
                    system_losses_pct=0.0,  # overridden by detailed_losses
                    inverter_efficiency_pct=inv_eff,
                    dc_ac_ratio=dc_ac_ratio,
                    albedo=albedo,
                    transposition_model=transposition,
                    module_type=selected_module,
                    detailed_losses=detailed,
                )
                st.success(get_text("sys_saved", lang))

    # ── Display current config ──────────────────────────────────────────
    if st.session_state.config is not None:
        with st.expander(get_text("sidebar_title", lang)):
            cfg = st.session_state.config
            st.json({
                "kWp": cfg.kwp,
                "tilt_deg": cfg.tilt_deg,
                "azimuth_deg": cfg.azimuth_deg,
                "inverter_efficiency_pct": cfg.inverter_efficiency_pct,
                "mode": st.session_state.config_mode,
            })

    # ── Navigation ──────────────────────────────────────────────────────
    render_nav_buttons("system_config", lang)
