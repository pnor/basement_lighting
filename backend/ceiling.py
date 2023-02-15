#!/usr/bin/env python3

import numpy as np
from typing import Any, Callable, List, Optional, Tuple
from typing_extensions import Self
import light_arrangements_python

from backend.backend_types import RGB
from backend.indexing import (
    cartesian_getitem,
    cartesian_setitem,
    float_cartesian_setitem,
    flaot_cartesian_getitem,
    float_polar_getitem,
    float_polar_setitem,
    linear_getitem,
    linear_setitem,
    polar_getitem,
    polar_setitem,
    row_getitem,
    row_setitem,
)
from backend.indexing_type import IndexingType


class Ceiling:
    def __init__(self, **kwargs):
        """
        Construct a wrapper around the light arrangement object
        """
        # -- Indexing
        self.indexing_type = IndexingType.LINEAR
        self._get_func = linear_getitem
        self._set_func = linear_setitem
        self._search_radius = 0
        self._set_radius = 0
        self._center = [0.5, 0.5]

        # Reading configs and instantiating the light arrangement
        self._rows = kwargs["rows"]
        light_arrangement_type = kwargs["type"]

        dimensions = kwargs["dimensions"]
        arrangement_file = kwargs["arrangement_file"]

        if light_arrangement_type == "test":
            sphere_size = kwargs["sphere_size"]
            camera_position = kwargs["camera_position"]
            dimension_mask = kwargs["dimension_mask"]

            self.light_arrangement = light_arrangements_python.init_test(
                dimensions,
                arrangement_file,
                sphere_size,
                camera_position,
                dimension_mask,
            )
        elif light_arrangement_type == "ws281x":
            number_lights = kwargs["number_lights"]
            io_pin = kwargs["io_pin"]

            self.light_arrangement = light_arrangements_python.init_ws281x(
                dimensions, arrangement_file, number_lights, io_pin
            )
        else:
            raise ValueError("invalid value: " + light_arrangement_type)

    # ===== Getting, Setting, Showing ==========
    def get_by_index(self, index: int) -> RGB:
        return np.array(self.light_arrangement.get_by_index(index))

    def set_by_index(self, index: int, color: RGB):
        self.light_arrangement.set_by_index(index, color)

    def get_closest(
        self, location: List[float], search_distance: float
    ) -> Optional[RGB]:
        res = self.light_arrangement.get_closest(location, search_distance)
        return np.array([0, 0, 0]) if res is None else np.array(res)

    def set_closest(self, location: List[float], search_distance: float, color: RGB):
        self.light_arrangement.set_closest(location, search_distance, color)

    def set_decreasing_intensity(
        self, location: List[float], fill_distance: float, color: RGB
    ):
        self.light_arrangement.set_decreasing_intensity(location, fill_distance, color)

    def set_decreasing_intensity_merge(
        self, location: List[float], fill_distance: float, color: RGB
    ):
        self.light_arrangement.set_decreasing_intensity_merge(
            location, fill_distance, color
        )

    def set_all_in_box(
        self, low_location: List[float], high_location: List[float], color: RGB
    ):
        self.light_arrangement.set_all_in_box(low_location, high_location, color)

    def set_all_in_radius(self, location: List[float], radius: float, color: RGB):
        self.light_arrangement.set_all_in_radius(location, radius, color)

    def clear(self) -> None:
        """Set every pixel to black (and updates the LEDs)"""
        self.light_arrangement.fill((0, 0, 0))

    def fill(self, clear_color: RGB) -> None:
        """Set every pixel to the given color"""
        self.light_arrangement.fill(clear_color)

    def show(self) -> None:
        """Update all pixels with updated colors at once"""
        self.light_arrangement.show()

    # ===== Metadata ==========
    def number_lights(self) -> int:
        return self.light_arrangement.number_lights()

    # ===== Getting / Setting ==========
    def __getitem__(self, key: Any) -> Optional[RGB]:
        pass

    def __setitem__(self, key: Any, value: RGB) -> None:
        pass

    def rows(self) -> Optional[List[int]]:
        """Returns rows information if the indexing is row indexing"""
        return self._rows

    # ===== Indexing ==========

    def use_linear(self):
        "Use linear indexing"
        self.indexing_type = IndexingType.LINEAR
        self._get_func = linear_getitem
        self._set_func = linear_setitem

    def with_linear(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the linear indexing method"""

        def _block():
            self.use_linear()
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def use_row(self):
        """Use row based indexing"""
        self.indexing_type = IndexingType.ROWS
        self._get_func = row_getitem
        self._set_func = row_setitem

    def with_row(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the row indexing method"""

        def _block():
            self.use_row()
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def use_cartesian(
        self,
        search_range: float = 0.2,
    ):
        """Use cartesian indexing"""
        self._search_radius = search_range
        self._set_radius = search_range
        self.indexing_type = IndexingType.CARTESIAN
        self._get_func = cartesian_getitem
        self._set_func = cartesian_setitem

    def with_cartesian(
        self,
        block: Callable[[Self], None],
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the cartesian indexing method"""

        def _block():
            self.use_cartesian(search_range=search_range)
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def use_polar(
        self,
        origin: List[float],
        search_range: float = 0.2,
    ):
        """Use polar indexing"""
        self._search_radius = search_range
        self._set_radius = search_range
        self._center = origin
        self.indexing_type = IndexingType.POLAR
        self._get_func = polar_getitem
        self._set_func = polar_setitem

    def with_polar(
        self,
        block: Callable[[Self], None],
        origin: List[float],
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the polar indexing method"""

        def _block():
            self.use_polar(origin, search_range=search_range)
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def use_float_cartesian(
        self,
        effect_radius: float = 0.2,
    ):
        """Use floating point cartesian indexing"""
        self._set_radius = effect_radius
        self.indexing_type = IndexingType.FLOAT_POLAR
        self._get_func = flaot_cartesian_getitem
        self._set_func = float_cartesian_setitem

    def with_float_cartesian(
        self,
        block: Callable[[Self], None],
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float cartesian indexing method"""

        def _block():
            self.use_float_cartesian(effect_radius=effect_radius)
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def use_float_polar(
        self,
        origin: List[float],
        effect_radius: float = 0.2,
    ):
        """Use floating point polar indexing"""
        self._search_radius = effect_radius
        self._set_radius = effect_radius
        self._center = origin
        self.indexing_type = IndexingType.FLOAT_POLAR
        self._get_func = float_polar_getitem
        self._set_func = float_polar_setitem

    def with_float_polar(
        self,
        block: Callable[[Self], None],
        origin: List[float],
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float polar indexing method"""

        def _block():
            self.use_float_polar(origin, effect_radius=effect_radius)
            block(self)

        self._run_block_save_indexing(lambda: _block())

    def _run_block_save_indexing(
        self,
        block: Callable[[], None],
    ):
        indexing_type = self.indexing_type
        get_func = self._get_func
        set_func = self._set_func
        search_radius = self._search_radius
        set_radius = self._set_radius
        center = self._center

        block()

        self.indexing_type = indexing_type
        self._get_func = get_func
        self._set_func = set_func
        self._search_radius = search_radius
        self._set_radius = set_radius
        self._center = center
