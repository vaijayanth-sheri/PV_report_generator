---
title: Solar PV Yield Calculator
emoji: ☀️
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# ☀️ Solar PV Yield Calculator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![pvlib](https://img.shields.io/badge/pvlib-0.10.3+-yellow.svg)](https://pvlib-python.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A production-ready web application built with Python and Streamlit that estimates solar photovoltaic (PV) energy yield. The application leverages the `pvlib` library for rigorous physics-based simulation and integrates with the PVGIS API to fetch location-specific Typical Meteorological Year (TMY) weather data. It provides users with an interactive KPI dashboard, visual analytics, and the ability to generate professional, bilingual PDF reports.

---

## 🚀 Features

- **Physics-Based Simulation**: Core engine powered by `pvlib`, handling solar position, Perez transposition, SAPM cell temperature, and DC/AC conversion.
- **Weather Data Integration**: REST API integration with PVGIS 5.3 to fetch hourly TMY meteorological data based on geocoded location (`geopy`).
- **Interactive UI**: Clean, modular Streamlit frontend with interactive map selection via `folium`.
- **Configurable Modes**: "Quick" mode for fast estimates, and "Pro" mode for detailed system control.
- **Bilingual Support (i18n)**: Fully localized in both English (EN) and German (DE).
- **Automated Reporting**: Generates client-ready, professional PDF summaries containing KPIs, monthly charts, and system assumptions using `ReportLab`.
- **Visual Analytics**: Interactive time-series and categorical charts using `Plotly`.

## 🏗️ Architecture

- **Frontend**: Streamlit, Plotly, Folium
- **Simulation Engine**: pvlib, pandas, numpy
- **Data APIs**: PVGIS API (weather data), Nominatim / geopy (geocoding)
- **PDF Engine**: ReportLab, Kaleido

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaijayanth-sheri/PV_report_generator.git
   cd PV_report_generator/solar_app
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the Streamlit application locally:

```bash
cd solar_app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`. 

## 🧪 Testing

The project uses `pytest` for unit testing. To run the tests:

```bash
cd solar_app
pytest tests/
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/vaijayanth-sheri/PV_report_generator/issues).

## 📝 License

This project is licensed under the MIT License.
