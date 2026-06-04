# Solar PV Yield Calculator

## 1. Executive Summary
A production-ready web application built with Python and Streamlit that estimates solar photovoltaic (PV) energy yield. The application leverages the `pvlib` library for rigorous physics-based simulation and integrates with the PVGIS API to fetch location-specific Typical Meteorological Year (TMY) weather data. It provides users with an interactive KPI dashboard, visual analytics, and the ability to generate professional, bilingual PDF reports.

## 2. Project Deep Dive
- **Domain**: Renewable Energy / Solar PV
- **Target Users**: Solar engineers, consultants, and renewable energy enthusiasts who need quick, reliable yield estimates.
- **Problem Statement**: There is a need for an accessible, professional tool that bridges the gap between complex physics-based solar simulation engines and user-friendly interfaces, while also automating client-ready report generation.
- **Architecture**: 
  - **Inputs**: Streamlit UI, Geocoding via `geopy` (Nominatim).
  - **Data Retrieval**: REST API integration with PVGIS 5.3 for hourly TMY data.
  - **Processing**: `pvlib` simulation engine handling solar position, Perez transposition, SAPM cell temperature, and DC/AC conversion.
  - **Output**: KPI Dashboard, Plotly interactive charts, and `ReportLab`-powered PDF generation.

## 3. Skills Extracted
- **Energy Systems Modeling**: Deep understanding of solar PV modeling, physics-based simulations, and irradiance transposition using `pvlib`.
- **Full Stack Python Development**: Building robust, interactive web interfaces using Streamlit with proper state management and routing.
- **API Integration**: Fetching and parsing external meteorological data from the PVGIS API.
- **Data Engineering & Analytics**: Processing time-series weather and energy data using `pandas` and `numpy`.
- **Data Visualization**: Creating interactive, insightful charts using `Plotly`.
- **Software Architecture**: Structuring a Python application with clean separation of concerns (views, services, models, config).
- **Internationalization (i18n)**: Implementing bilingual support (English/German) across the UI and generated reports.

## 4. Resume Material
- **Developed a Solar PV Yield Calculator** using Python, Streamlit, and `pvlib`, enabling physics-based PV modeling and TMY weather data integration via the PVGIS API.
- **Engineered a comprehensive reporting module** with `ReportLab`, generating bilingual (EN/DE) PDF reports featuring KPIs, monthly production charts, and system assumptions for client presentations.
- **Designed a clean, modular software architecture** separating UI components, simulation engines, and external API services, ensuring maintainability and scalability.

## 5. Portfolio Writeup
**Solar PV Yield Calculator**
This project is an end-to-end tool designed for solar energy professionals. It bridges the gap between complex physics-based simulations (using `pvlib`) and an accessible user interface (built with Streamlit). Users can seamlessly geocode their location, fetch site-specific Typical Meteorological Year (TMY) data from PVGIS, and configure system parameters via Quick or Pro modes. The application instantly visualizes performance metrics such as annual yield, capacity factor, and performance ratio. A standout feature is the automated PDF report generation, which produces clean, bilingual, client-ready summaries of the energy yield.

## 6. LinkedIn Version
I recently built a Solar PV Yield Calculator! ☀️ 
Developed with Python, Streamlit, and `pvlib`, this web app fetches real PVGIS weather data and runs physics-based simulations to estimate solar energy production anywhere in the supported regions. It features interactive charts and even generates bilingual PDF reports for clients. It was a great experience combining data engineering, renewable energy modeling, and full-stack development into one seamless tool. 
#SolarEnergy #Python #RenewableEnergy #Streamlit #DataScience #pvlib

## 7. Interview Talking Points
- **Situation**: There was a need to quickly estimate solar PV yield and generate professional, client-facing reports without relying on expensive or overly complex desktop software.
- **Task**: Build an accessible, web-based application that handles physics-based PV modeling, weather data retrieval, and automated reporting.
- **Action**: I built the app using Streamlit for the frontend, integrated the PVGIS API for weather data, and utilized `pvlib` for the core simulation engine. I also implemented `ReportLab` to dynamically generate bilingual PDF reports.
- **Result**: Delivered a modular, production-ready tool that allows users to configure PV systems (with Quick and Pro modes) and download detailed performance reports, demonstrating strong product ownership and software engineering skills.

## 8. Hidden Value Report
- **Product Ownership**: The thoughtful inclusion of "Quick" and "Pro" modes shows a deep understanding of different user personas—from casual users wanting a quick estimate to engineers needing detailed control.
- **Market Readiness**: Built-in English and German support demonstrates an awareness of international markets and the importance of localization.
- **Clean Architecture**: Despite Streamlit's script-based nature, the project is structured with a clear separation of concerns (e.g., `views/`, `services/`, `models/`), showcasing mature software design principles.
