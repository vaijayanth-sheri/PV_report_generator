"""
Step 1 — Location selection page.

Allows the user to:
  - Search by city, street, postal code, or free-form address
  - Click on an interactive map to drop a pin
  - Enter coordinates manually
  - Confirm and store the location in session state
"""

from __future__ import annotations

import streamlit as st
import folium
from streamlit_folium import st_folium

from config.translations import get_text
from services.geocode import geocode_address, search_addresses
from services.validation import validate_coordinates
from views.nav_buttons import render_nav_buttons


def render_location_page(lang: str) -> None:
    """Render the location selection page."""
    st.header(get_text("loc_title", lang))

    # Default coordinates (Munich) if nothing is set yet
    default_lat = st.session_state.latitude if st.session_state.latitude is not None else 48.1351
    default_lon = st.session_state.longitude if st.session_state.longitude is not None else 11.5820

    # ── Address search ──────────────────────────────────────────────────
    st.subheader(get_text("loc_address_label", lang))
    st.caption({
        "en": "Search by city name, street address, postal code, or any combination.",
        "de": "Suche nach Stadtname, Straßenadresse, Postleitzahl oder einer beliebigen Kombination.",
    }[lang])

    col_addr, col_btn = st.columns([4, 1])
    with col_addr:
        address = st.text_input(
            get_text("loc_address_label", lang),
            value="",
            label_visibility="collapsed",
            placeholder={
                "en": "e.g. Munich, Marienplatz 1, or 80331",
                "de": "z.B. München, Marienplatz 1 oder 80331",
            }[lang],
        )
    with col_btn:
        search_clicked = st.button(
            get_text("loc_search_btn", lang),
            use_container_width=True,
            type="primary",
        )

    if search_clicked and address.strip():
        with st.spinner("🔍 Geocoding…"):
            results = search_addresses(address.strip(), limit=5)

        if results:
            # If multiple results, let the user pick
            if len(results) > 1:
                options = {r.display_name: r for r in results}
                selected_name = st.selectbox(
                    {
                        "en": "Multiple results found — select one:",
                        "de": "Mehrere Ergebnisse gefunden — bitte auswählen:",
                    }[lang],
                    options=list(options.keys()),
                )
                selected = options[selected_name]
            else:
                selected = results[0]

            st.session_state.latitude = selected.latitude
            st.session_state.longitude = selected.longitude
            st.session_state.location_name = selected.display_name
            default_lat = selected.latitude
            default_lon = selected.longitude
            st.success(
                get_text("loc_success", lang, lat=selected.latitude, lon=selected.longitude)
            )
        else:
            st.warning(get_text("loc_not_found", lang))

    # ── Interactive map — click to drop pin ──────────────────────────────
    st.subheader({
        "en": "📌 Select location on map",
        "de": "📌 Standort auf der Karte auswählen",
    }[lang])
    st.caption({
        "en": "Click anywhere on the map to place a pin at that location.",
        "de": "Klicken Sie auf die Karte, um einen Pin an dieser Position zu setzen.",
    }[lang])

    # Build folium map
    m = folium.Map(location=[default_lat, default_lon], zoom_start=10)

    # Add a marker for the current location
    if st.session_state.latitude is not None:
        folium.Marker(
            [st.session_state.latitude, st.session_state.longitude],
            popup=st.session_state.location_name or "Selected Location",
            icon=folium.Icon(color="red", icon="solar-panel", prefix="fa"),
        ).add_to(m)

    # Render the map and capture click events
    map_data = st_folium(
        m,
        width=None,
        height=450,
        returned_objects=["last_clicked"],
    )

    # Handle map click → update coordinates
    if map_data and map_data.get("last_clicked"):
        clicked_lat = round(map_data["last_clicked"]["lat"], 6)
        clicked_lon = round(map_data["last_clicked"]["lng"], 6)

        if (clicked_lat != st.session_state.latitude or
                clicked_lon != st.session_state.longitude):
            st.session_state.latitude = clicked_lat
            st.session_state.longitude = clicked_lon
            st.session_state.location_name = f"{clicked_lat:.4f}°N, {clicked_lon:.4f}°E"
            st.rerun()

    # ── Manual coordinate input ─────────────────────────────────────────
    with st.expander(get_text("loc_manual_label", lang)):
        col_lat, col_lon = st.columns(2)
        with col_lat:
            manual_lat = st.number_input(
                get_text("loc_lat", lang),
                min_value=-90.0,
                max_value=90.0,
                value=default_lat,
                step=0.01,
                format="%.4f",
            )
        with col_lon:
            manual_lon = st.number_input(
                get_text("loc_lon", lang),
                min_value=-180.0,
                max_value=180.0,
                value=default_lon,
                step=0.01,
                format="%.4f",
            )

        if st.button(get_text("loc_confirm_btn", lang)):
            errors = validate_coordinates(manual_lat, manual_lon)
            if errors:
                for err_key in errors:
                    st.error(get_text(err_key, lang))
            else:
                st.session_state.latitude = manual_lat
                st.session_state.longitude = manual_lon
                st.session_state.location_name = f"{manual_lat:.4f}°N, {manual_lon:.4f}°E"
                st.success(
                    get_text("loc_success", lang, lat=manual_lat, lon=manual_lon)
                )
                st.rerun()

    # ── Current selection summary ───────────────────────────────────────
    if st.session_state.latitude is not None:
        st.info(
            f"📍 **{get_text('sidebar_location', lang)}:** "
            f"{st.session_state.location_name}  \n"
            f"**{get_text('loc_lat', lang)}:** {st.session_state.latitude:.4f}° | "
            f"**{get_text('loc_lon', lang)}:** {st.session_state.longitude:.4f}°"
        )

    # ── Navigation ──────────────────────────────────────────────────────
    render_nav_buttons("location", lang)
