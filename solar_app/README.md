# Solar PV Yield Calculator

A modular, production-ready Streamlit application for solar photovoltaic energy yield estimation using **pvlib** and **PVGIS TMY** weather data.

## Features

- **PVGIS Integration** — Fetches Typical Meteorological Year (TMY) hourly data from the official PVGIS 5.3 API
- **pvlib Simulation Engine** — Full physics-based PV modeling (solar position, Perez transposition, SAPM cell temperature, PVWatts DC/AC)
- **Quick & Pro Modes** — Simplified configuration for rapid estimates, or detailed engineering parameters for professionals
- **KPI Dashboard** — Annual yield, specific yield, capacity factor, performance ratio
- **Interactive Charts** — Monthly production bar charts via Plotly
- **PDF Report Generation** — Professional multi-page report with cover page, KPIs, tables, charts, methodology, and assumptions
- **Bilingual Support** — Full English / German language toggle (UI + reports)
- **CSV Export** — Download hourly simulation results

## Project Structure

```
solar_app/
├── app.py                  # Streamlit entry point
├── pages/
│   ├── location.py         # Step 1: Location selection (geocoding + map)
│   ├── weather.py          # Step 2: PVGIS TMY data retrieval
│   ├── system_config.py    # Step 3: Quick / Pro system configuration
│   ├── results.py          # Step 4: Simulation results & KPIs
│   └── report_page.py      # Step 5: PDF report generation
├── services/
│   ├── pvgis_client.py     # PVGIS TMY API client
│   ├── geocode.py          # Address → coordinates (Nominatim)
│   └── validation.py       # Input validation utilities
├── models/
│   ├── pv_model.py         # pvlib simulation engine
│   └── assumptions.py      # Configuration dataclasses
├── report/
│   ├── report_generator.py # ReportLab PDF builder
│   └── templates/          # Future template assets
├── config/
│   └── translations.py     # EN/DE bilingual dictionary
├── tests/
│   └── test_basic.py       # Unit tests
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
cd solar_app
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Running Tests

```bash
python -m pytest tests/test_basic.py -v
```

## Workflow

1. **Location** — Search by address or enter coordinates manually
2. **Weather** — Fetch PVGIS TMY hourly data for the selected site
3. **System** — Configure PV system parameters (Quick or Pro mode)
4. **Results** — Run the pvlib simulation and view KPIs + monthly chart
5. **Report** — Generate and download a professional PDF report

## Known Limitations

- **Weather data** is based on Typical Meteorological Year (TMY) and does not reflect actual conditions for any specific year
- **No near-shading analysis** — only far-shading via loss parameters
- **Module degradation** is applied as a fixed first-year loss, not a multi-year model
- **Grid availability and curtailment** are not modeled
- **Module/inverter selection** in Pro Mode uses simplified technology categories rather than specific product databases
- **PVGIS coverage** is limited to Europe, Africa, the Mediterranean, and parts of Asia/South America

## Future Roadmap

- [ ] Integration with CEC/Sandia module & inverter databases for detailed component selection
- [ ] Multi-array / multi-orientation support
- [ ] Near-shading analysis with horizon profile
- [ ] Financial analysis (LCOE, NPV, payback period)
- [ ] Battery storage modeling
- [ ] Custom PDF templates (HTML/CSS based)
- [ ] User account system with saved projects
- [ ] API endpoint for batch simulations
- [ ] Satellite imagery integration for roof area estimation

## Technology Stack

| Component | Library |
|-----------|---------|
| UI Framework | Streamlit |
| PV Modeling | pvlib |
| Weather Data | PVGIS 5.3 API |
| Charts | Plotly |
| PDF Reports | ReportLab |
| Geocoding | geopy (Nominatim) |
| Data | pandas, numpy |

## License

This project is provided as-is for educational and professional demonstration purposes.
