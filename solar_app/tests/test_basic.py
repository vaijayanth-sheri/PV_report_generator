"""
Basic test suite for the Solar PV Report Generator.

Tests core modules without requiring live API calls.
Run with:  python -m pytest tests/test_basic.py -v
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# 1. Translation completeness
# ---------------------------------------------------------------------------
from config.translations import TRANSLATIONS, get_text


class TestTranslations:
    """Verify translation dictionary integrity."""

    def test_all_keys_have_en_and_de(self):
        for key, entry in TRANSLATIONS.items():
            assert "en" in entry, f"Key '{key}' missing English translation"
            assert "de" in entry, f"Key '{key}' missing German translation"

    def test_get_text_returns_string(self):
        result = get_text("app_title", "en")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_text_fallback_to_key(self):
        result = get_text("nonexistent_key_xyz", "en")
        assert result == "nonexistent_key_xyz"

    def test_get_text_interpolation(self):
        result = get_text("loc_success", "en", lat=48.0, lon=11.0)
        assert "48.0000" in result
        assert "11.0000" in result


# ---------------------------------------------------------------------------
# 2. Dataclass construction
# ---------------------------------------------------------------------------
from models.assumptions import (
    DetailedLosses,
    ProConfig,
    QuickConfig,
    SimulationResult,
)


class TestDataclasses:
    """Verify configuration dataclass construction and defaults."""

    def test_quick_config_defaults(self):
        cfg = QuickConfig()
        assert cfg.kwp == 5.0
        assert cfg.tilt_deg == 30.0
        assert cfg.azimuth_deg == 180.0
        assert 0 <= cfg.system_losses_pct <= 100
        assert 0 <= cfg.inverter_efficiency_pct <= 100

    def test_pro_config_inherits_quick(self):
        cfg = ProConfig(kwp=10.0)
        assert cfg.kwp == 10.0
        assert hasattr(cfg, "dc_ac_ratio")
        assert hasattr(cfg, "albedo")
        assert hasattr(cfg, "transposition_model")

    def test_detailed_losses_combined(self):
        losses = DetailedLosses()
        combined = losses.combined_loss_fraction
        assert 0.0 < combined < 1.0

    def test_pro_effective_losses_with_detailed(self):
        losses = DetailedLosses(soiling_pct=5.0, shading_pct=5.0)
        cfg = ProConfig(detailed_losses=losses)
        eff = cfg.effective_system_losses_pct
        assert eff > 0

    def test_simulation_result_defaults(self):
        result = SimulationResult()
        assert result.annual_yield_kwh == 0.0
        assert len(result.monthly_yield_kwh) == 12


# ---------------------------------------------------------------------------
# 3. Validation
# ---------------------------------------------------------------------------
from services.validation import (
    validate_coordinates,
    validate_pro_config,
    validate_system_config,
)


class TestValidation:
    """Verify validation logic."""

    def test_valid_coordinates(self):
        assert validate_coordinates(48.0, 11.0) == []

    def test_invalid_latitude(self):
        errors = validate_coordinates(95.0, 11.0)
        assert len(errors) > 0

    def test_invalid_longitude(self):
        errors = validate_coordinates(48.0, 200.0)
        assert len(errors) > 0

    def test_valid_system_config(self):
        errors = validate_system_config(5.0, 30.0, 180.0, 14.0, 96.0)
        assert errors == []

    def test_invalid_kwp(self):
        errors = validate_system_config(0.0, 30.0, 180.0, 14.0, 96.0)
        assert len(errors) > 0

    def test_valid_pro_config(self):
        errors = validate_pro_config(1.2, 0.2)
        assert errors == []

    def test_invalid_albedo(self):
        errors = validate_pro_config(1.2, 1.5)
        assert len(errors) > 0


# ---------------------------------------------------------------------------
# 4. PVGIS URL (no live call)
# ---------------------------------------------------------------------------
from services.pvgis_client import PVGIS_BASE_URL


class TestPVGIS:
    """Verify PVGIS constants (no live API calls)."""

    def test_base_url_format(self):
        assert "re.jrc.ec.europa.eu" in PVGIS_BASE_URL
        assert "tmy" in PVGIS_BASE_URL


# ---------------------------------------------------------------------------
# 5. PV Model with synthetic data
# ---------------------------------------------------------------------------
from models.pv_model import run_simulation


class TestPVModel:
    """Run the simulation engine with synthetic weather data."""

    @staticmethod
    def _make_synthetic_weather() -> pd.DataFrame:
        """Create a minimal synthetic 8760-row weather DataFrame."""
        idx = pd.date_range("2005-01-01", periods=8760, freq="h", tz="UTC")
        hours = np.arange(8760)
        # Crude diurnal pattern
        hour_of_day = hours % 24
        ghi = np.where((hour_of_day >= 6) & (hour_of_day <= 18),
                       300 * np.sin(np.pi * (hour_of_day - 6) / 12), 0).astype(float)
        dni = ghi * 0.7
        dhi = ghi * 0.3
        temp = 15.0 + 10.0 * np.sin(2 * np.pi * hours / 8760)
        ws = np.full(8760, 3.0)

        return pd.DataFrame({
            "ghi": ghi,
            "dni": dni,
            "dhi": dhi,
            "temp_air": temp,
            "wind_speed": ws,
        }, index=idx)

    def test_simulation_runs(self):
        weather = self._make_synthetic_weather()
        config = QuickConfig(kwp=5.0)
        result = run_simulation(weather, 48.1351, 11.5820, config)

        assert result.annual_yield_kwh > 0
        assert len(result.monthly_yield_kwh) == 12
        assert result.specific_yield_kwh_kwp > 0
        assert 0 < result.capacity_factor_pct < 100
        assert 0 < result.performance_ratio_pct < 200  # Allow generous range for synthetic data

    def test_simulation_pro_mode(self):
        weather = self._make_synthetic_weather()
        config = ProConfig(kwp=10.0, dc_ac_ratio=1.3)
        result = run_simulation(weather, 48.1351, 11.5820, config)

        assert result.annual_yield_kwh > 0
        assert result.hourly_ac_power_w is not None
        assert len(result.hourly_ac_power_w) == 8760
