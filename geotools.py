# https://geographiclib.sourceforge.io/html/python/geodesics.html#solution-of-geodesic-problems
from geographiclib.geodesic import Geodesic
import numpy as np

import config


def compute_lat_lon(px: float, py: float) -> tuple:
    """
    Compute the position in the global WGS84 coordinate reference system.

    :param float px: X coordinate in the indoor positioning system.
    :param float py: Y coordinate in the indoor positioning system.
    :return: Point (px, py) as (latitude,longitude).
    :rtype: tuple

    """
    lat1 = config.ORIGIN_LAT
    lon1 = config.ORIGIN_LON

    # Azimuth angle with respect to the vertical axis of the WGS84
    # reference system.
    alpha = np.rad2deg(np.arctan2(py, px))
    azi1 = 90.0 - alpha - np.abs(config.DELTA_AZIMUTH)
    if azi1 > 180.0:
        azi1 = azi1 - 360.0

    # Distance between the origin and point (px,py).
    s12 = np.sqrt(np.power(px, 2) + np.power(py, 2))

    # Solve a direct geodesic problem.
    solution = Geodesic.WGS84.Direct(lat1, lon1, azi1, s12)
    latitude = round(solution["lat2"], 8)
    longitude = round(solution["lon2"], 8)

    return (latitude, longitude)


def compute_xyz(lat2: float, lon2: float, height: float) -> tuple:
    """
    Compute the position in the local coordinate reference system.

    :param float lat2: Latitude.
    :param float lon2: Longitude.
    :param float height: Height.
    :return: Coordinates as (px,py).
    :rtype: tuple

    """
    lat1 = config.ORIGIN_LAT
    lon1 = config.ORIGIN_LON
    hmsl = config.ORIGIN_HMSL

    # Solve an inverse geodesic problem.
    solution = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
    distance = solution["s12"]
    azimuth = solution["azi1"]

    # Angle with respect to the positive X axis of the indoor position system.
    angle = np.deg2rad(90.0 - azimuth - np.abs(config.DELTA_AZIMUTH))

    # Compute the position (px,py).
    px = distance * np.cos(angle)
    py = distance * np.sin(angle)
    pz = height - hmsl

    return (px, py, pz)
