"""
Bilingual translation store for the Solar PV Report Generator.

All UI strings, report labels, and section titles are keyed by a stable
identifier and stored for English (en) and German (de).  The active
language is selected at runtime via Streamlit session state.

Usage:
    from config.translations import get_text, TRANSLATIONS
    label = get_text("app_title", lang="de")
"""

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
# Master translation dictionary
# ---------------------------------------------------------------------------
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ── General / App-wide ──────────────────────────────────────────────
    "app_title": {
        "en": "Solar PV Yield Calculator",
        "de": "Solar-PV-Ertragsrechner",
    },
    "language_label": {
        "en": "Language",
        "de": "Sprache",
    },
    "nav_location": {
        "en": "📍 Location",
        "de": "📍 Standort",
    },
    "nav_weather": {
        "en": "🌤️ Weather Data",
        "de": "🌤️ Wetterdaten",
    },
    "nav_system": {
        "en": "⚙️ System Configuration",
        "de": "⚙️ Systemkonfiguration",
    },
    "nav_results": {
        "en": "📊 Results",
        "de": "📊 Ergebnisse",
    },
    "nav_report": {
        "en": "📄 Report",
        "de": "📄 Bericht",
    },
    "nav_back": {
        "en": "Back",
        "de": "Zurück",
    },
    "nav_next": {
        "en": "Next",
        "de": "Weiter",
    },
    # ── Sidebar ─────────────────────────────────────────────────────────
    "sidebar_title": {
        "en": "Configuration Summary",
        "de": "Konfigurationsübersicht",
    },
    "sidebar_location": {
        "en": "Location",
        "de": "Standort",
    },
    "sidebar_lat": {
        "en": "Latitude",
        "de": "Breitengrad",
    },
    "sidebar_lon": {
        "en": "Longitude",
        "de": "Längengrad",
    },
    "sidebar_kwp": {
        "en": "System Size (kWp)",
        "de": "Anlagengröße (kWp)",
    },
    "sidebar_tilt": {
        "en": "Tilt (°)",
        "de": "Neigung (°)",
    },
    "sidebar_azimuth": {
        "en": "Azimuth (°)",
        "de": "Azimut (°)",
    },
    "sidebar_mode": {
        "en": "Mode",
        "de": "Modus",
    },
    "sidebar_weather_status": {
        "en": "Weather Data",
        "de": "Wetterdaten",
    },
    "sidebar_loaded": {
        "en": "Loaded ✅",
        "de": "Geladen ✅",
    },
    "sidebar_not_loaded": {
        "en": "Not loaded",
        "de": "Nicht geladen",
    },
    # ── Location Page ───────────────────────────────────────────────────
    "loc_title": {
        "en": "Step 1: Select Location",
        "de": "Schritt 1: Standort auswählen",
    },
    "loc_address_label": {
        "en": "Search by address",
        "de": "Nach Adresse suchen",
    },
    "loc_manual_label": {
        "en": "Or enter coordinates manually",
        "de": "Oder Koordinaten manuell eingeben",
    },
    "loc_search_btn": {
        "en": "Search",
        "de": "Suchen",
    },
    "loc_confirm_btn": {
        "en": "Confirm Location",
        "de": "Standort bestätigen",
    },
    "loc_lat": {
        "en": "Latitude",
        "de": "Breitengrad",
    },
    "loc_lon": {
        "en": "Longitude",
        "de": "Längengrad",
    },
    "loc_success": {
        "en": "Location confirmed: {lat:.4f}°N, {lon:.4f}°E",
        "de": "Standort bestätigt: {lat:.4f}°N, {lon:.4f}°E",
    },
    "loc_not_found": {
        "en": "Address not found. Please try a different query.",
        "de": "Adresse nicht gefunden. Bitte versuchen Sie eine andere Eingabe.",
    },
    # ── Weather Page ────────────────────────────────────────────────────
    "weather_title": {
        "en": "Step 2: Weather Data (PVGIS TMY)",
        "de": "Schritt 2: Wetterdaten (PVGIS TMY)",
    },
    "weather_fetch_btn": {
        "en": "Fetch TMY Data",
        "de": "TMY-Daten abrufen",
    },
    "weather_fetching": {
        "en": "Fetching data from PVGIS…",
        "de": "Daten werden von PVGIS abgerufen…",
    },
    "weather_success": {
        "en": "TMY data loaded — {rows} hourly records.",
        "de": "TMY-Daten geladen — {rows} Stundenwerte.",
    },
    "weather_fail": {
        "en": "Failed to fetch weather data: {error}",
        "de": "Wetterdaten konnten nicht abgerufen werden: {error}",
    },
    "weather_preview": {
        "en": "Data Preview",
        "de": "Datenvorschau",
    },
    "weather_stats": {
        "en": "Summary Statistics",
        "de": "Zusammenfassung",
    },
    "weather_location_missing": {
        "en": "⚠️ Please select a location first (Step 1).",
        "de": "⚠️ Bitte wählen Sie zuerst einen Standort (Schritt 1).",
    },
    "weather_ghi": {
        "en": "Global Horizontal Irradiance (W/m²)",
        "de": "Globale Horizontalstrahlung (W/m²)",
    },
    "weather_dni": {
        "en": "Direct Normal Irradiance (W/m²)",
        "de": "Direktnormalstrahlung (W/m²)",
    },
    "weather_dhi": {
        "en": "Diffuse Horizontal Irradiance (W/m²)",
        "de": "Diffuse Horizontalstrahlung (W/m²)",
    },
    "weather_temp": {
        "en": "Ambient Temperature (°C)",
        "de": "Umgebungstemperatur (°C)",
    },
    "weather_wind": {
        "en": "Wind Speed (m/s)",
        "de": "Windgeschwindigkeit (m/s)",
    },
    # ── System Config Page ──────────────────────────────────────────────
    "sys_title": {
        "en": "Step 3: System Configuration",
        "de": "Schritt 3: Systemkonfiguration",
    },
    "sys_mode_quick": {
        "en": "Quick Mode",
        "de": "Schnellmodus",
    },
    "sys_mode_pro": {
        "en": "Pro Mode",
        "de": "Profimodus",
    },
    "sys_kwp": {
        "en": "System Size (kWp)",
        "de": "Anlagengröße (kWp)",
    },
    "sys_tilt": {
        "en": "Tilt Angle (°)",
        "de": "Neigungswinkel (°)",
    },
    "sys_azimuth": {
        "en": "Azimuth (°, 180=South)",
        "de": "Azimut (°, 180=Süd)",
    },
    "sys_losses": {
        "en": "System Losses (%)",
        "de": "Systemverluste (%)",
    },
    "sys_inv_eff": {
        "en": "Inverter Efficiency (%)",
        "de": "Wechselrichter-Wirkungsgrad (%)",
    },
    "sys_dc_ac": {
        "en": "DC/AC Ratio",
        "de": "DC/AC-Verhältnis",
    },
    "sys_albedo": {
        "en": "Ground Albedo",
        "de": "Bodenalbedo",
    },
    "sys_transposition": {
        "en": "Transposition Model",
        "de": "Transpositionsmodell",
    },
    "sys_module_type": {
        "en": "Module Technology",
        "de": "Modultechnologie",
    },
    "sys_confirm_btn": {
        "en": "Save Configuration",
        "de": "Konfiguration speichern",
    },
    "sys_saved": {
        "en": "Configuration saved ✅",
        "de": "Konfiguration gespeichert ✅",
    },
    "sys_losses_soiling": {
        "en": "Soiling Loss (%)",
        "de": "Verschmutzungsverlust (%)",
    },
    "sys_losses_shading": {
        "en": "Shading Loss (%)",
        "de": "Verschattungsverlust (%)",
    },
    "sys_losses_mismatch": {
        "en": "Mismatch Loss (%)",
        "de": "Mismatch-Verlust (%)",
    },
    "sys_losses_wiring": {
        "en": "Wiring Loss (%)",
        "de": "Verkabelungsverlust (%)",
    },
    "sys_losses_aging": {
        "en": "Aging/Degradation (%)",
        "de": "Alterung/Degradation (%)",
    },
    # ── Results Page ────────────────────────────────────────────────────
    "res_title": {
        "en": "Step 4: Simulation Results",
        "de": "Schritt 4: Simulationsergebnisse",
    },
    "res_run_btn": {
        "en": "Run Simulation",
        "de": "Simulation starten",
    },
    "res_running": {
        "en": "Running pvlib simulation…",
        "de": "pvlib-Simulation läuft…",
    },
    "res_annual_yield": {
        "en": "Annual Yield (kWh)",
        "de": "Jahresertrag (kWh)",
    },
    "res_specific_yield": {
        "en": "Specific Yield (kWh/kWp)",
        "de": "Spezifischer Ertrag (kWh/kWp)",
    },
    "res_capacity_factor": {
        "en": "Capacity Factor (%)",
        "de": "Kapazitätsfaktor (%)",
    },
    "res_performance_ratio": {
        "en": "Performance Ratio (%)",
        "de": "Performance Ratio (%)",
    },
    "res_monthly_chart_title": {
        "en": "Monthly Energy Production (kWh)",
        "de": "Monatliche Energieproduktion (kWh)",
    },
    "res_month": {
        "en": "Month",
        "de": "Monat",
    },
    "res_energy_kwh": {
        "en": "Energy (kWh)",
        "de": "Energie (kWh)",
    },
    "res_download_csv": {
        "en": "Download Results (CSV)",
        "de": "Ergebnisse herunterladen (CSV)",
    },
    "res_missing_config": {
        "en": "⚠️ Please complete Steps 1–3 before running simulation.",
        "de": "⚠️ Bitte schließen Sie die Schritte 1–3 ab, bevor Sie die Simulation starten.",
    },
    # ── Report Page ─────────────────────────────────────────────────────
    "rpt_title": {
        "en": "Step 5: Generate Report",
        "de": "Schritt 5: Bericht erstellen",
    },
    "rpt_generate_btn": {
        "en": "Generate PDF Report",
        "de": "PDF-Bericht erstellen",
    },
    "rpt_download_btn": {
        "en": "Download Report",
        "de": "Bericht herunterladen",
    },
    "rpt_generating": {
        "en": "Generating report…",
        "de": "Bericht wird erstellt…",
    },
    "rpt_missing_results": {
        "en": "⚠️ Please run the simulation first (Step 4).",
        "de": "⚠️ Bitte führen Sie zuerst die Simulation durch (Schritt 4).",
    },
    # ── Report PDF content ──────────────────────────────────────────────
    "rpt_cover_title": {
        "en": "Solar PV Yield Assessment Report",
        "de": "Solar-PV-Ertragsanalyse-Bericht",
    },
    "rpt_cover_subtitle": {
        "en": "Generated with PV Report Generator",
        "de": "Erstellt mit dem PV-Berichtsgenerator",
    },
    "rpt_exec_summary": {
        "en": "Executive Summary",
        "de": "Zusammenfassung",
    },
    "rpt_monthly_table": {
        "en": "Monthly Production",
        "de": "Monatliche Produktion",
    },
    "rpt_config_summary": {
        "en": "System Configuration",
        "de": "Systemkonfiguration",
    },
    "rpt_methodology": {
        "en": "Methodology",
        "de": "Methodik",
    },
    "rpt_assumptions": {
        "en": "Assumptions & Limitations",
        "de": "Annahmen & Einschränkungen",
    },
    "rpt_methodology_text": {
        "en": (
            "This report was generated using pvlib, an open-source Python library "
            "for photovoltaic energy modeling. Weather data is sourced from PVGIS "
            "(Photovoltaic Geographical Information System) Typical Meteorological "
            "Year (TMY) dataset provided by the European Commission Joint Research "
            "Centre.\n\n"
            "The simulation pipeline includes:\n"
            "• Solar position calculation (NREL SPA algorithm)\n"
            "• Plane-of-array irradiance transposition (Perez model by default)\n"
            "• Cell temperature estimation (SAPM model)\n"
            "• DC power output (PVWatts model)\n"
            "• AC conversion via constant inverter efficiency or PVWatts inverter model\n"
            "• Monthly and annual energy yield aggregation"
        ),
        "de": (
            "Dieser Bericht wurde mit pvlib erstellt, einer Open-Source-Python-"
            "Bibliothek für die Photovoltaik-Energiemodellierung. Die Wetterdaten "
            "stammen aus dem PVGIS (Photovoltaic Geographical Information System) "
            "Typical Meteorological Year (TMY) Datensatz des Joint Research Centre "
            "der Europäischen Kommission.\n\n"
            "Die Simulationspipeline umfasst:\n"
            "• Sonnenstandsberechnung (NREL SPA-Algorithmus)\n"
            "• Transposition der Einstrahlungsdaten (standardmäßig Perez-Modell)\n"
            "• Zelltemperaturabschätzung (SAPM-Modell)\n"
            "• DC-Leistungsberechnung (PVWatts-Modell)\n"
            "• AC-Umwandlung über konstanten Wirkungsgrad oder PVWatts-Wechselrichtermodell\n"
            "• Monatliche und jährliche Ertragsaggregation"
        ),
    },
    "rpt_assumptions_text": {
        "en": (
            "• Weather data represents a Typical Meteorological Year and may not "
            "reflect actual conditions in any specific year.\n"
            "• System losses are applied as a single derating factor unless "
            "detailed losses are specified in Pro Mode.\n"
            "• No near-shading analysis is performed.\n"
            "• Module degradation over time is not modeled unless explicitly set.\n"
            "• Grid availability and curtailment are not considered.\n"
            "• Results are estimates and should be validated with on-site measurements "
            "for financial decisions."
        ),
        "de": (
            "• Die Wetterdaten repräsentieren ein typisches meteorologisches Jahr "
            "und spiegeln möglicherweise nicht die tatsächlichen Bedingungen eines "
            "bestimmten Jahres wider.\n"
            "• Systemverluste werden als einzelner Minderungsfaktor angewendet, es "
            "sei denn, detaillierte Verluste sind im Profimodus angegeben.\n"
            "• Es wird keine Nahverschattungsanalyse durchgeführt.\n"
            "• Die Moduldegradation über die Zeit wird nicht modelliert, sofern "
            "nicht explizit festgelegt.\n"
            "• Netzverfügbarkeit und Abregelung werden nicht berücksichtigt.\n"
            "• Die Ergebnisse sind Schätzungen und sollten für finanzielle "
            "Entscheidungen durch Vor-Ort-Messungen validiert werden."
        ),
    },
    # ── Month names ─────────────────────────────────────────────────────
    "month_names": {
        "en": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ],
        "de": [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember",
        ],
    },
    # ── Validation ──────────────────────────────────────────────────────
    "val_lat_range": {
        "en": "Latitude must be between -90 and 90.",
        "de": "Breitengrad muss zwischen -90 und 90 liegen.",
    },
    "val_lon_range": {
        "en": "Longitude must be between -180 and 180.",
        "de": "Längengrad muss zwischen -180 und 180 liegen.",
    },
    "val_kwp_positive": {
        "en": "System size must be greater than 0.",
        "de": "Anlagengröße muss größer als 0 sein.",
    },
    "val_tilt_range": {
        "en": "Tilt must be between 0 and 90 degrees.",
        "de": "Neigung muss zwischen 0 und 90 Grad liegen.",
    },
    "val_azimuth_range": {
        "en": "Azimuth must be between 0 and 360 degrees.",
        "de": "Azimut muss zwischen 0 und 360 Grad liegen.",
    },
    "val_losses_range": {
        "en": "Losses must be between 0 and 100 percent.",
        "de": "Verluste müssen zwischen 0 und 100 Prozent liegen.",
    },
}


def get_text(key: str, lang: str = "en", **kwargs: object) -> str:
    """Return the translated string for *key* in the requested *lang*.

    Supports ``str.format()`` keyword interpolation when **kwargs are given.

    Falls back to English if the requested language is missing,
    and returns the key itself if the key is not found.
    """
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass  # Return unformatted string on template mismatch
    return text
