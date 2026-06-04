"""
Input validation utilities.

Provides validation functions for user inputs used across the
Location, System Configuration, and Weather pages.  Each function
returns a list of human-readable error messages (empty = valid).
"""

from __future__ import annotations

from typing import List


def validate_coordinates(latitude: float, longitude: float) -> List[str]:
    """Validate geographic coordinates.

    Returns
    -------
    list[str]
        List of validation error messages (empty if valid).
    """
    errors: List[str] = []
    if not -90.0 <= latitude <= 90.0:
        errors.append("val_lat_range")
    if not -180.0 <= longitude <= 180.0:
        errors.append("val_lon_range")
    return errors


def validate_system_config(
    kwp: float,
    tilt_deg: float,
    azimuth_deg: float,
    system_losses_pct: float,
    inverter_efficiency_pct: float,
) -> List[str]:
    """Validate Quick Mode system configuration parameters.

    Returns
    -------
    list[str]
        List of translation keys for validation errors.
    """
    errors: List[str] = []

    if kwp <= 0:
        errors.append("val_kwp_positive")
    if not 0.0 <= tilt_deg <= 90.0:
        errors.append("val_tilt_range")
    if not 0.0 <= azimuth_deg <= 360.0:
        errors.append("val_azimuth_range")
    if not 0.0 <= system_losses_pct <= 100.0:
        errors.append("val_losses_range")
    if not 0.0 <= inverter_efficiency_pct <= 100.0:
        errors.append("val_losses_range")

    return errors


def validate_pro_config(
    dc_ac_ratio: float,
    albedo: float,
) -> List[str]:
    """Validate additional Pro Mode parameters.

    Returns
    -------
    list[str]
        List of translation keys for validation errors.
    """
    errors: List[str] = []

    if dc_ac_ratio <= 0:
        errors.append("DC/AC ratio must be greater than 0.")
    if not 0.0 <= albedo <= 1.0:
        errors.append("Albedo must be between 0 and 1.")

    return errors
