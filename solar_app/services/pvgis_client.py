"""
PVGIS TMY data client.

Fetches Typical Meteorological Year (TMY) hourly data from the official
PVGIS 5.3 API (Joint Research Centre, European Commission).

Reference:
    https://re.jrc.ec.europa.eu/api/v5_3/
"""

from __future__ import annotations

import io
import logging
from typing import Dict, Optional, Tuple

import pandas as pd
import requests

logger = logging.getLogger(__name__)

# PVGIS v5.3 TMY endpoint
PVGIS_BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_3/tmy"

# Expected number of hourly rows in a TMY year
EXPECTED_ROWS = 8760

# HTTP timeout in seconds
REQUEST_TIMEOUT = 60


def fetch_tmy_data(
    latitude: float,
    longitude: float,
    *,
    startyear: int = 2005,
    endyear: int = 2020,
    timeout: int = REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """Fetch TMY hourly weather data from PVGIS.

    Parameters
    ----------
    latitude : float
        Site latitude in decimal degrees (-90 to 90).
    longitude : float
        Site longitude in decimal degrees (-180 to 180).
    startyear : int
        Start year for TMY selection window.
    endyear : int
        End year for TMY selection window.
    timeout : int
        HTTP request timeout in seconds.

    Returns
    -------
    pd.DataFrame
        DataFrame with DatetimeIndex (UTC) and columns:
        ``ghi``, ``dni``, ``dhi``, ``temp_air``, ``wind_speed``,
        ``ir_diffuse`` (infrared), ``relative_humidity``.

    Raises
    ------
    PVGISError
        If the API call fails or the response is invalid.
    """
    params: Dict[str, object] = {
        "lat": latitude,
        "lon": longitude,
        "startyear": startyear,
        "endyear": endyear,
        "outputformat": "csv",
    }

    logger.info("Requesting PVGIS TMY for (%.4f, %.4f)", latitude, longitude)

    try:
        response = requests.get(
            PVGIS_BASE_URL, params=params, timeout=timeout
        )
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise PVGISError(
            f"PVGIS request timed out after {timeout}s."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise PVGISError(
            f"PVGIS HTTP error: {exc.response.status_code} — {exc.response.text[:300]}"
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise PVGISError(f"PVGIS connection error: {exc}") from exc

    df = _parse_csv_response(response.text)
    df = _validate_and_clean(df)
    return df


def _parse_csv_response(raw_csv: str) -> pd.DataFrame:
    """Parse the PVGIS CSV response into a DataFrame.

    PVGIS CSV output contains header lines before the actual data and
    trailing metadata.  We locate the data block between the first line
    starting with ``time`` and the first subsequent blank line.
    """
    lines = raw_csv.strip().splitlines()

    # Find the header line (starts with "time(")
    header_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("time("):
            header_idx = i
            break

    if header_idx is None:
        raise PVGISError("Could not locate data header in PVGIS response.")

    # Find the end of the data block (first empty or metadata line)
    data_end = len(lines)
    for i in range(header_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped == "" or not stripped[0].isdigit():
            data_end = i
            break

    data_block = "\n".join(lines[header_idx:data_end])
    df = pd.read_csv(io.StringIO(data_block))

    # Rename the time column
    time_col = df.columns[0]
    df = df.rename(columns={time_col: "time"})

    return df


def _validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Validate row count, parse timestamps, rename columns, handle NaNs."""

    # ── Parse timestamp ─────────────────────────────────────────────────
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M", utc=True)
    df = df.set_index("time").sort_index()

    # ── Standardise column names ────────────────────────────────────────
    col_map = {
        "G(h)": "ghi",
        "Gb(n)": "dni",
        "Gd(h)": "dhi",
        "T2m": "temp_air",
        "WS10m": "wind_speed",
        "IR(h)": "ir_diffuse",
        "RH": "relative_humidity",
        "SP": "pressure",
    }
    df = df.rename(columns=col_map)

    # ── Validate expected row count ─────────────────────────────────────
    if len(df) < EXPECTED_ROWS:
        logger.warning(
            "PVGIS returned %d rows (expected %d). Missing hours will be interpolated.",
            len(df),
            EXPECTED_ROWS,
        )
        # Resample to hourly and interpolate gaps
        df = df.resample("h").interpolate(method="linear")

    if len(df) > EXPECTED_ROWS:
        logger.info("Trimming PVGIS data to %d rows.", EXPECTED_ROWS)
        df = df.iloc[:EXPECTED_ROWS]

    # ── Handle remaining NaN values ─────────────────────────────────────
    nan_count = df.isna().sum().sum()
    if nan_count > 0:
        logger.warning("Filling %d NaN values via forward-fill.", nan_count)
        df = df.ffill().bfill()

    # ── Ensure numeric types ────────────────────────────────────────────
    numeric_cols = ["ghi", "dni", "dhi", "temp_air", "wind_speed"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Final NaN sweep after coercion
    df = df.ffill().bfill()

    logger.info("PVGIS TMY data ready: %d rows, columns=%s", len(df), list(df.columns))
    return df


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------
class PVGISError(Exception):
    """Raised when PVGIS data retrieval or parsing fails."""
