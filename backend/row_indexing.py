#!/usr/bin/env python3

from typing import Union, Tuple, Optional, List
from backend.indexing import Indexing

from backend.backend_types import RGB
from backend.indexing import Indexing
from backend.neopixel_wrapper import PixelWrapper


class RowIndexing(Indexing):
    """
    Index into the light strip based on how they are arranged into rows.
    """

    def __init__(self, pixels: PixelWrapper, lights_per_row: List[int]):
        self._pixels = pixels
        self.rows = lights_per_row

    def get(self, key: Tuple[int, int]) -> Optional[RGB]:
        """key: (row, col)"""
        row, col = key
        return self._pixels[self.row_col_to_indx(row, col)]

    def set(self, key: Union[Tuple[int, int], int], newvalue: RGB) -> None:
        """
        key: (row, col) or row
        if key is a tuple, will set one LED. If key is an int corresponding to the row, will set
        every LED in the row
        """
        if type(key) is tuple and len(key) == 2:
            row, col = key
            self._pixels[self.row_col_to_indx(row, col)] = newvalue
        elif type(key) is int:
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

    def prepare_to_send(self):
        pass
