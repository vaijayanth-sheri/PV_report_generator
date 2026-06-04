"""
Geocoding service.

Converts address strings (city, street, postal code, etc.) into
(latitude, longitude) coordinates.  Uses the OpenStreetMap Nominatim
API via direct HTTP requests for maximum reliability.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
GEOCODE_TIMEOUT = 10
USER_AGENT = "SolarPVReportGenerator/1.0 (educational-project)"


@dataclass
class GeoLocation:
    """Geocoded location result."""
    latitude: float
    longitude: float
    display_name: str


def geocode_address(address: str, timeout: int = GEOCODE_TIMEOUT) -> Optional[GeoLocation]:
    """Resolve an address string to geographic coordinates.

    Supports cities, streets, postal codes, and free-form queries.

    Parameters
    ----------
    address : str
        Free-form address (e.g., "Munich, Germany", "10115 Berlin",
        "Marienplatz 1, München").
    timeout : int
        HTTP request timeout in seconds.

    Returns
    -------
    GeoLocation or None
        The resolved location, or ``None`` if the address could not be found.
    """
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en",
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        logger.warning("Geocoding timed out for: %s", address)
        return None
    except requests.exceptions.RequestException as exc:
        logger.error("Geocoding request failed: %s", exc)
        return None
    except ValueError:
        logger.error("Invalid JSON response from geocoder")
        return None

    if not data:
        logger.info("No geocoding result for: %s", address)
        return None

    hit = data[0]
    result = GeoLocation(
        latitude=round(float(hit["lat"]), 6),
        longitude=round(float(hit["lon"]), 6),
        display_name=hit.get("display_name", address),
    )
    logger.info("Geocoded '%s' → (%.6f, %.6f)", address, result.latitude, result.longitude)
    return result


def search_addresses(query: str, limit: int = 5, timeout: int = GEOCODE_TIMEOUT) -> List[GeoLocation]:
    """Return multiple geocoding results for autocomplete-style search.

    Parameters
    ----------
    query : str
        Partial or full address string.
    limit : int
        Maximum number of results to return.

    Returns
    -------
    list[GeoLocation]
        List of matching locations.
    """
    params = {
        "q": query,
        "format": "json",
        "limit": limit,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en",
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        logger.error("Search request failed: %s", exc)
        return []

    results = []
    for hit in data:
        results.append(GeoLocation(
            latitude=round(float(hit["lat"]), 6),
            longitude=round(float(hit["lon"]), 6),
            display_name=hit.get("display_name", query),
        ))
    return results
