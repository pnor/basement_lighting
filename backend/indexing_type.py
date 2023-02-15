#!/usr/bin/env python3


from enum import Enum


class IndexingType(Enum):
    LINEAR = 0
    ROWS = 1
    CARTESIAN = 2
    POLAR = 3
    FLOAT_CARTESIAN = 5
    FLOAT_POLAR = 6
