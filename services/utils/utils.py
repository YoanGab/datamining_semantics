from typing import Optional
from urllib.parse import quote

import numpy as np
import requests


def convert_kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def get_extension_from_format(format: str) -> str:
    """ Get the extension from the format
    :param format: the format
    :return: the extension
    """
    if format == 'xml':
        return 'xml'
    elif format == 'n3':
        return 'n3'
    elif format == 'turtle':
        return 'ttl'
    elif format == 'nt':
        return 'nt'
    elif format == 'pretty-xml':
        return 'xml'
    elif format == 'trix':
        return 'trix'
    elif format == 'trig':
        return 'trig'
    elif format == 'nquads':
        return 'nq'
    else:
        return 'xml'


def get_euclidean_distance(x: list, y: list) -> float:
    """Get the euclidean distance between two points.
    :param x: the first point
    :param y: the second point
    :return: the distance
    """
    x = np.array(x)
    y = np.array(y)
    return np.linalg.norm(x - y)


def find_nearest_station(coordinates: list, available_stations: list) -> dict:
    """Find the nearest station to the given coordinates.

    :param coordinates: the coordinates
    :param available_stations: the available stations
    :return: the nearest station
    """
    nearest_departure: Optional[dict] = None
    distance_departure: Optional[float] = None
    for station in available_stations:
        distance: float = get_euclidean_distance(
            coordinates,
            [station['latitude'], station['longitude']]
        )
        if not distance_departure or distance < distance_departure:
            distance_departure = distance
            nearest_departure = station
    return nearest_departure


def get_coordinates_from_address(address: str) -> list:
    """Get the coordinates from the address.
    :param address: the address
    :return: the coordinates
    """
    url: str = f"https://api-adresse.data.gouv.fr/search/?q={quote(address)}"
    json_response: dict = requests.get(url).json()

    return json_response['features'][0]['geometry']['coordinates'][::-1]
