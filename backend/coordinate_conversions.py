#!/usr/bin/env python3

import light_arrangements_python
from typing import List


def polar(rho: float, angular_coords: List[float], center: List[float]) -> List[float]:
    return light_arrangements_python.Loc2.polar(rho, angular_coords, center)


def cylindrical(
    radius: float, theta: float, coords: List[float], center: List[float]
) -> List[float]:
    return light_arrangements_python.Loc2.cylindrical(radius, theta, coords, center)
