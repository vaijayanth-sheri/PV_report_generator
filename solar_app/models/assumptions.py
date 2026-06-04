"""
Data models for PV system configuration and simulation results.

Uses Python dataclasses for clean, typed configuration handling.
Two configuration modes are supported:
  - QuickConfig:  simplified inputs for rapid estimates
  - ProConfig:    extends QuickConfig with detailed engineering parameters

All physical defaults are realistic values commonly used in the European
PV industry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Quick Mode configuration
# ---------------------------------------------------------------------------
@dataclass
class QuickConfig:
    """Simplified PV system configuration.

    Attributes:
        kwp:                System DC nameplate capacity in kilo-watt peak.
        tilt_deg:           Module tilt from horizontal (0‑90°).
        azimuth_deg:        Module azimuth in degrees (0=N, 90=E, 180=S, 270=W).
        system_losses_pct:  Aggregate system losses as a single percentage (0‑100).
                            Includes soiling, mismatch, wiring, etc.
        inverter_efficiency_pct: Inverter conversion efficiency (0‑100).
    """
    kwp: float = 5.0
    tilt_deg: float = 30.0
    azimuth_deg: float = 180.0          # South-facing
    system_losses_pct: float = 14.0     # PVGIS default for crystalline Si
    inverter_efficiency_pct: float = 96.0


# ---------------------------------------------------------------------------
# Detailed loss breakdown (Pro Mode)
# ---------------------------------------------------------------------------
@dataclass
class DetailedLosses:
    """Individual loss components in percent.

    When supplied, the effective system loss is computed as the
    product of (1 - loss_i/100) for all components.
    """
    soiling_pct: float = 2.0
    shading_pct: float = 3.0
    mismatch_pct: float = 2.0
    wiring_dc_pct: float = 2.0
    wiring_ac_pct: float = 0.5
    aging_pct: float = 1.5  # First-year degradation

    @property
    def combined_loss_fraction(self) -> float:
        """Return the combined loss as a fraction (0‑1)."""
        remaining = 1.0
        for loss_pct in [
            self.soiling_pct,
            self.shading_pct,
            self.mismatch_pct,
            self.wiring_dc_pct,
            self.wiring_ac_pct,
            self.aging_pct,
        ]:
            remaining *= 1.0 - loss_pct / 100.0
        return 1.0 - remaining


# ---------------------------------------------------------------------------
# Pro Mode configuration
# ---------------------------------------------------------------------------
@dataclass
class ProConfig(QuickConfig):
    """Extended PV system configuration for advanced users.

    Inherits all QuickConfig fields and adds detailed engineering
    parameters.  When *detailed_losses* is provided, it overrides
    *system_losses_pct* from the parent class.
    """
    dc_ac_ratio: float = 1.2
    albedo: float = 0.2               # Typical ground albedo
    transposition_model: str = "perez"  # Options: perez, isotropic, haydavies, klucher
    module_type: str = "crystalline_silicon"  # Options: crystalline_silicon, thin_film, cdte
    detailed_losses: Optional[DetailedLosses] = None

    # Temperature model coefficients (SAPM open_rack_glass_polymer)
    temp_model_params: str = "open_rack_glass_polymer"

    @property
    def effective_system_losses_pct(self) -> float:
        """Return the effective system loss percentage.

        Uses detailed losses if provided, otherwise falls back to
        the aggregate *system_losses_pct*.
        """
        if self.detailed_losses is not None:
            return self.detailed_losses.combined_loss_fraction * 100.0
        return self.system_losses_pct


# ---------------------------------------------------------------------------
# Module technology parameters
# ---------------------------------------------------------------------------
MODULE_TYPES: Dict[str, Dict[str, float]] = {
    "crystalline_silicon": {
        "gamma_pdc": -0.004,   # %/°C power temperature coefficient
        "description_en": "Crystalline Silicon (mono/poly)",
        "description_de": "Kristallines Silizium (mono/poly)",
    },
    "thin_film": {
        "gamma_pdc": -0.002,
        "description_en": "Thin Film (CIS/CIGS)",
        "description_de": "Dünnschicht (CIS/CIGS)",
    },
    "cdte": {
        "gamma_pdc": -0.003,
        "description_en": "Cadmium Telluride (CdTe)",
        "description_de": "Cadmiumtellurid (CdTe)",
    },
}


# ---------------------------------------------------------------------------
# Simulation result container
# ---------------------------------------------------------------------------
@dataclass
class SimulationResult:
    """Container for PV simulation output.

    Attributes:
        annual_yield_kwh:      Total AC energy over the TMY year (kWh).
        monthly_yield_kwh:     List of 12 monthly AC yields (kWh).
        specific_yield_kwh_kwp: Annual yield divided by system kWp.
        capacity_factor_pct:   Ratio of actual output to theoretical max (%).
        performance_ratio_pct: Ratio of actual yield to yield at STC irradiance (%).
        hourly_ac_power_w:     Hourly AC power time-series (W), for CSV export.
        poa_global_kwh_m2:     Total plane-of-array irradiance (kWh/m²/year).
    """
    annual_yield_kwh: float = 0.0
    monthly_yield_kwh: List[float] = field(default_factory=lambda: [0.0] * 12)
    specific_yield_kwh_kwp: float = 0.0
    capacity_factor_pct: float = 0.0
    performance_ratio_pct: float = 0.0
    hourly_ac_power_w: Optional[List[float]] = None
    poa_global_kwh_m2: float = 0.0
