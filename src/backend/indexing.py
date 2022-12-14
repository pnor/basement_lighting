#!/usr/bin/env python3

from neopixel import NeoPixel
from typing import Any, Tuple, List, Union

from backend.backend_types import RGB

"""
Abstraction of how indexing gets and sets indeces
"""


class Indexing:
    """
    Abstract class representing how getting indeces and setting indeces operate
    """

    def __init__(self):
        pass

    def get(self, key: Any) -> RGB:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")
        return (0, 0, 0)

    def set(self, key: Any, newvalue: RGB) -> None:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")
        pass


class LinearIndexing(Indexing):
    """Index into the light strip based on their order in sequence.
    This is the default way NeoPixels indexes the lights."""

    def __init__(self, pixels: NeoPixel):
        self._pixels = pixels

    def get(self, key: int) -> RGB:
        return self._pixels[key]

    def set(self, key: int, newvalue: RGB) -> None:
        self._pixels[key] = newvalue


class RowIndexing(Indexing):
    """
    Index into the light strip based on how they are arranged into rows.
    """

    def __init__(self, pixels: NeoPixel, lights_per_row: List[int]):
        self._pixels = pixels
        self.rows = lights_per_row

    def get(self, key: Tuple[int, int]) -> RGB:
        """key: (row, col)"""
        row, col = key
        return self._pixels[self.row_col_to_indx(row, col)]

    def set(self, key: Union[Tuple[int, int], int], newvalue: RGB) -> None:
        """
        key: (row, col) or row
        if key is a tuple, will set one LED. If key is an int corresponding to the row, will set
        every LED in the row
        """
        if type(key) == tuple:
            row, col = key
            self._pixels[self.row_col_to_indx(row, col)] = newvalue
        elif type(key) == int:
            row = key
            for i in range(self.rows[row]):
                self._pixels[self.row_col_to_indx(row, i)] = newvalue
        else:
            raise NotImplementedError("key for row indexing was neither tuple or int")

    def row_col_to_indx(self, row: int, col: int) -> int:
        """Convert row and col position to index in light strip"""
        row = row % len(self.rows)
        indx = sum(self.rows[:row])
        if row % 2 == 0:
            indx += col
        else:
            indx += self.rows[row] - col
        return indx


class CartesianIndexing(Indexing):
    """Index into the light strip as a grid on 2D space.
    This is done by mapping lights in sequence to integer 2 dimensional coordinates.

    Assumes rows of LEDs are layed out like this:
    --->
     \
      \
    ----
    """

    # https://pypi.org/project/hqt/
    # quadtree for later
    def __init__(self, pixels: NeoPixel, rows: int, cols: int):
        self._pixels = pixels
        self.ROWS = rows
        self.COLS = cols

    def get(self, key: Tuple[int, int]) -> RGB:
        """key: (x, y)"""
        # TODO
        return [0, 0, 0]

    def set(self, key: Tuple[int, int], newvalue: RGB) -> None:
        """key: (x, y)"""
        # TODO
        pass


class PolarIndexing(Indexing):
    """
    Index into the light strip using polar coordinates.
    Will select the single nearest LED, assuming origin is at the center of the grid formed by the LEDs
    """

    # NOTE: thinking, wherever the polar coords end up, select the closest of the 4 points around
    # it. Have a check if its v out of bounds ofc

    def __init__(self, pixels: NeoPixel, rows: int, cols: int):
        self._pixels = pixels
        self.ROWS = rows
        self.COLS = cols

    def get(self, key: Tuple[float, float]) -> RGB:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key
        return [0, 0, 0]

    def set(self, key: Tuple[float, float], newvalue: RGB) -> None:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key


class FloatCartesianIndexing(Indexing):
    """Index into the light strip with floats as a grid on 2D space.
    Setting a decimal index will spread the light effect on nearby lights"""

    def __init__(self, pixels: NeoPixel, rows: int, cols: int):
        self._pixels = pixels
        self.ROWS = rows
        self.COLS = cols

    def get(self, key: Tuple[float, float]) -> RGB:
        """key: (x, y)"""
        # TODO
        return [0, 0, 0]

    def set(self, key: Tuple[float, float], newvalue: RGB) -> None:
        """key: (x, y)"""
        # TODO
        pass


class FloatPolarIndexing(Indexing):
    """
    Index into the light strip using float polar coordinates.
    If the index lies between multiple LEDs (not an integer) will spread the light effect on nearby lights
    """

    # NOTE: thinking, wherever the polar coords end up, select the closest of the 4 points around
    # it. Have a check if its v out of bounds ofc

    def __init__(self, pixels: NeoPixel, rows: int, cols: int):
        self._pixels = pixels
        self.ROWS = rows
        self.COLS = cols

    def get(self, key: Tuple[float, float]) -> RGB:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key
        return [0, 0, 0]

    def set(self, key: Tuple[float, float], newvalue: RGB) -> None:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key
