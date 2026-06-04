"""
PV simulation engine using pvlib.

Implements the full pvlib-based simulation pipeline:
    1. Solar position (NREL SPA via pvlib.solarposition)
    2. Plane-of-array irradiance transposition (Perez default)
    3. Cell temperature (SAPM model)
    4. DC power output (PVWatts model)
    5. AC power conversion
    6. KPI computation (annual/monthly yield, specific yield, capacity factor, PR)

All physical parameters use realistic industry defaults.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd
import pvlib
from pvlib.location import Location
from pvlib.irradiance import get_total_irradiance
from pvlib.temperature import sapm_cell

from models.assumptions import (
    MODULE_TYPES,
    ProConfig,
    QuickConfig,
    SimulationResult,
)

logger = logging.getLogger(__name__)


def run_simulation(
    weather_df: pd.DataFrame,
    latitude: float,
    longitude: float,
    config: QuickConfig,
) -> SimulationResult:
    """Run a complete PV yield simulation.

    Parameters
    ----------
    weather_df : pd.DataFrame
        Hourly weather data with DatetimeIndex (UTC) and columns:
        ``ghi``, ``dni``, ``dhi``, ``temp_air``, ``wind_speed``.
    latitude : float
        Site latitude in decimal degrees.
    longitude : float
        Site longitude in decimal degrees.
    config : QuickConfig or ProConfig
        System configuration dataclass.

    Returns
    -------
    SimulationResult
        Aggregated simulation results including annual yield, monthly
        breakdown, and KPI metrics.
    """
    logger.info("Starting PV simulation — %.2f kWp at (%.4f, %.4f)", config.kwp, latitude, longitude)

    # ── Resolve configuration ───────────────────────────────────────────
    is_pro = isinstance(config, ProConfig)
    albedo = config.albedo if is_pro else 0.2
    transposition_model = config.transposition_model if is_pro else "perez"
    module_type = config.module_type if is_pro else "crystalline_silicon"
    gamma_pdc = MODULE_TYPES.get(module_type, MODULE_TYPES["crystalline_silicon"])["gamma_pdc"]
    dc_ac_ratio = config.dc_ac_ratio if is_pro else 1.2

    if is_pro:
        system_losses_fraction = config.effective_system_losses_pct / 100.0
    else:
        system_losses_fraction = config.system_losses_pct / 100.0

    inverter_eff = config.inverter_efficiency_pct / 100.0
    system_capacity_w = config.kwp * 1000.0  # Convert kWp to Wp

    # ── 1. Solar position ───────────────────────────────────────────────
    site = Location(latitude, longitude, tz="UTC")
    solpos = site.get_solarposition(weather_df.index)
    solar_zenith = solpos["apparent_zenith"]
    solar_azimuth = solpos["azimuth"]

    # Filter out nighttime (zenith > 90°) for cleaner computation
    # We keep all rows but let pvlib handle negative power naturally

    # ── 2. Plane-of-array irradiance ────────────────────────────────────
    # Compute extraterrestrial DNI (required by Perez and other anisotropic models)
    dni_extra = pvlib.irradiance.get_extra_radiation(weather_df.index)

    # Compute air mass for Perez model
    airmass = site.get_airmass(weather_df.index, solar_position=solpos)
    airmass_abs = airmass["airmass_absolute"]

    poa = get_total_irradiance(
        surface_tilt=config.tilt_deg,
        surface_azimuth=config.azimuth_deg,
        solar_zenith=solar_zenith,
        solar_azimuth=solar_azimuth,
        dni=weather_df["dni"],
        ghi=weather_df["ghi"],
        dhi=weather_df["dhi"],
        dni_extra=dni_extra,
        airmass=airmass_abs,
        albedo=albedo,
        model=transposition_model,
    )

    poa_global = poa["poa_global"].clip(lower=0.0).fillna(0.0)

    # ── 3. Cell temperature (SAPM) ──────────────────────────────────────
    temp_params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]

    if is_pro and config.temp_model_params in temp_params:
        temp_config = temp_params[config.temp_model_params]
    else:
        temp_config = temp_params["open_rack_glass_polymer"]

    cell_temp = sapm_cell(
        poa_global=poa_global,
        temp_air=weather_df["temp_air"],
        wind_speed=weather_df["wind_speed"],
        a=temp_config["a"],
        b=temp_config["b"],
        deltaT=temp_config["deltaT"],
    )

    # ── 4. DC power output (PVWatts) ────────────────────────────────────
    dc_power = pvlib.pvsystem.pvwatts_dc(
        g_poa_effective=poa_global,
        temp_cell=cell_temp,
        pdc0=system_capacity_w,
        gamma_pdc=gamma_pdc,
        temp_ref=25.0,
    )

    # Apply system losses
    dc_power_after_losses = dc_power * (1.0 - system_losses_fraction)

    # ── 5. AC power conversion ──────────────────────────────────────────
    # Apply inverter efficiency and clip to inverter AC rating
    inverter_capacity_w = system_capacity_w / dc_ac_ratio
    ac_power = dc_power_after_losses.clip(lower=0.0) * inverter_eff
    ac_power = ac_power.clip(upper=inverter_capacity_w)

    # ── 6. Aggregate results ────────────────────────────────────────────
    hourly_energy_kwh = ac_power / 1000.0  # Wh → kWh (hourly data)

    annual_yield = float(hourly_energy_kwh.sum())
    monthly_yield = hourly_energy_kwh.groupby(hourly_energy_kwh.index.month).sum()
    monthly_list = [float(monthly_yield.get(m, 0.0)) for m in range(1, 13)]

    specific_yield = annual_yield / config.kwp if config.kwp > 0 else 0.0

    # Capacity factor: actual output / (rated power × 8760 hours)
    max_annual_kwh = config.kwp * 8760.0
    capacity_factor = (annual_yield / max_annual_kwh * 100.0) if max_annual_kwh > 0 else 0.0

    # Performance ratio: actual yield / reference yield
    # Reference yield = POA irradiance (kWh/m²) × system kWp / 1 kW/m² (STC)
    poa_total_kwh_m2 = float(poa_global.sum()) / 1000.0  # Wh/m² → kWh/m²
    reference_yield = poa_total_kwh_m2 * config.kwp  # kWh at STC
    performance_ratio = (annual_yield / reference_yield * 100.0) if reference_yield > 0 else 0.0

    result = SimulationResult(
        annual_yield_kwh=round(annual_yield, 1),
        monthly_yield_kwh=[round(v, 1) for v in monthly_list],
        specific_yield_kwh_kwp=round(specific_yield, 1),
        capacity_factor_pct=round(capacity_factor, 2),
        performance_ratio_pct=round(performance_ratio, 2),
        hourly_ac_power_w=[round(float(v), 2) for v in ac_power.tolist()],
        poa_global_kwh_m2=round(poa_total_kwh_m2, 1),
    )

    logger.info(
        "Simulation complete — Annual yield: %.1f kWh, Specific yield: %.1f kWh/kWp, PR: %.1f%%",
        result.annual_yield_kwh,
        result.specific_yield_kwh_kwp,
        result.performance_ratio_pct,
    )

    return result
