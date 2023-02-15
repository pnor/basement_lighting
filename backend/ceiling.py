#!/usr/bin/env python3

# from typing import Callable, Any, Optional, List, Tuple
# from typing_extensions import Self
# from backend.cartesian_indexing import CartesianIndexing
# from backend.float_cartesian import FloatCartesianIndexing
# from backend.float_polar import FloatPolarIndexing
# from backend.led_locations import LEDSpace
# from backend.linear_indexing import LinearIndexing
# from backend.neopixel_wrapper import (
#     init_for_testing,
#     init_with_real_board,
# )
# from backend.polar_indexing import PolarIndexing
# from backend.row_indexing import RowIndexing
#
#
# from .backend_types import RGB
#
# from .indexing import *
import light_arrangements_python


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

    # ===== Animation / Clearing ==========

    def clear(self, show=True) -> None:
        """Set every pixel to black (and updates the LEDs)"""
        self.fill([0, 0, 0])
        if show:
            self.show()

    def fill(self, clear_color: RGB) -> None:
        """Set every pixel to the given color"""
        self._pixels.fill(clear_color)

    def show(self) -> None:
        """Update all pixels with updated colors at once"""
        self._pixels.show()

    # ===== Getting / Setting ==========
    def __getitem__(self, key: Any) -> Optional[RGB]:
        return self._indexing.get(key)

    def __setitem__(self, key: Any, value: RGB) -> None:
        self._indexing.set(key, value)

    def rows(self) -> Optional[List[int]]:
        """Returns rows information if the indexing is row indexing"""
        if isinstance(self._indexing, RowIndexing):
            return self._indexing.rows
        else:
            return None

    def testing_mode_rows(self, lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT):
        self._pixels.set_lights_per_row(lights_per_row)

    def indexing(self) -> Indexing:
        """Return the current Indexing object"""
        return self._indexing

    # ===== Async and Sending Between Processes ==========

    def prepare_to_send(self) -> None:
        """
        Prepares the ceiling object to be sent between processes with `Pipe`
        Must call this before sending this with `pipe.send(ceiling)`!
        """
        self._cached_led_spacing = None
        self._pixels.prepare_to_send()
        self._indexing.prepare_to_send()

    # ===== Indexing ==========

    def use_linear(self):
        "Use linear indexing"
        self._indexing = LinearIndexing(self._pixels)

    def with_linear(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the linear indexing method"""
        old_indexing = self._indexing
        self.use_linear()
        block(self)
        self._indexing = old_indexing

    def use_row(self, lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT):
        """Use row based indexing"""
        self._indexing = RowIndexing(self._pixels, lights_per_row)

    def with_row(self, block: Callable[[Self], None]) -> None:
        """Execute `block` with the row indexing method"""
        old_indexing = self._indexing
        self.use_row()
        block(self)
        self._indexing = old_indexing

    def use_cartesian(
        self,
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        search_range: float = 0.2,
    ):
        """Use cartesian indexing"""
        self._indexing = CartesianIndexing(
            self._pixels,
            lights_per_row,
            search_range,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def with_cartesian(
        self,
        block: Callable[[Self], None],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the cartesian indexing method"""
        old_indexing = self._indexing
        self.use_cartesian(lights_per_row, search_range)
        block(self)
        self._indexing = old_indexing

    def use_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        search_range: float = 0.2,
    ):
        assert len(origin) == 2
        """Use polar indexing"""
        self._indexing = PolarIndexing(
            self._pixels,
            lights_per_row=lights_per_row,
            origin=origin,
            search_range=search_range,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def with_polar(
        self,
        block: Callable[[Self], None],
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        search_range: float = 0.2,
    ) -> None:
        """Execute `block` with the polar indexing method"""
        old_indexing = self._indexing
        self.use_polar(origin, lights_per_row, search_range=search_range)
        block(self)
        self._indexing = old_indexing

    def use_float_cartesian(
        self,
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point cartesian indexing"""
        self._indexing = FloatCartesianIndexing(
            self._pixels,
            lights_per_row,
            effect_radius=effect_radius,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def with_float_cartesian(
        self,
        block: Callable[[Self], None],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float cartesian indexing method"""
        old_indexing = self._indexing
        self.use_float_cartesian(lights_per_row, effect_radius)
        block(self)
        self._indexing = old_indexing

    def use_float_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point polar indexing"""
        self._indexing = FloatPolarIndexing(
            self._pixels,
            lights_per_row,
            origin,
            effect_radius=effect_radius,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def with_float_polar(
        self,
        block: Callable[[Self], None],
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ) -> None:
        """Execute `block` with the float polar indexing method"""
        old_indexing = self._indexing
        self.use_float_polar(origin, lights_per_row, effect_radius)
        block(self)
        self._indexing = old_indexing
