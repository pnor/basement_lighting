#!/usr/bin/env python3

import numpy as np
from typing import Any, Callable, List, Optional, Tuple
from typing_extensions import Self
import light_arrangements_python

from backend.backend_types import RGB


class Ceiling:
    def __init__(self, **kwargs):
        """
        Construct a wrapper around the light arrangement object
        """
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

    def clear(self) -> None:
        """Set every pixel to black (and updates the LEDs)"""
        self.light_arrangement.fill((0, 0, 0))

    def fill(self, clear_color: RGB) -> None:
        """Set every pixel to the given color"""
        self.light_arrangement.fill(clear_color)

    def show(self) -> None:
        """Update all pixels with updated colors at once"""
        self.light_arrangement.show()

    # ===== Getting / Setting ==========
    def __getitem__(self, key: Any) -> Optional[RGB]:
        pass

    def __setitem__(self, key: Any, value: RGB) -> None:
        pass

    def rows(self) -> Optional[List[int]]:
        """Returns rows information if the indexing is row indexing"""
        pass

    # ===== Indexing ==========

    def use_linear(self):
        "Use linear indexing"
        pass

    def with_linear(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the linear indexing method"""
        pass

    def use_row(self, lights_per_row: List[int]):
        """Use row based indexing"""
        pass

    def with_row(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the row indexing method"""
        pass

    def use_cartesian(
        self,
        lights_per_row: List[int],
        search_range: float = 0.2,
    ):
        """Use cartesian indexing"""
        pass

    def with_cartesian(
        self,
        block: Callable[[Self], None],
        lights_per_row: List[int],
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the cartesian indexing method"""
        pass

    def use_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int],
        search_range: float = 0.2,
    ):
        """Use polar indexing"""
        pass

    def with_polar(
        self,
        block: Callable[[Self], None],
        origin: Tuple[float, float],
        lights_per_row: List[int],
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the polar indexing method"""
        pass

    def use_float_cartesian(
        self,
        lights_per_row: List[int],
        effect_radius: float = 0.2,
    ):
        """Use floating point cartesian indexing"""
        pass

    def with_float_cartesian(
        self,
        block: Callable[[Self], None],
        lights_per_row: List[int],
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float cartesian indexing method"""
        pass

    def use_float_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int],
        effect_radius: float = 0.2,
    ):
        """Use floating point polar indexing"""
        pass

    def with_float_polar(
        self,
        block: Callable[[Self], None],
        origin: Tuple[float, float],
        lights_per_row: List[int],
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float polar indexing method"""
        pass
