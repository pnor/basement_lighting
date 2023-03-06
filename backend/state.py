#!/usr/bin/env python3

import backend.ceiling

from typing import Optional
from multiprocessing import Process, Pipe
from threading import Lock

from backend.settings import Settings

Ceiling = backend.ceiling.Ceiling


class State:
    def __init__(self) -> None:
        self.settings = Settings("settings.toml")

        self.current_process: Optional[Process] = None
        self.current_pattern: Optional[str] = None
        self.lock = Lock()

    def create_ceiling(self) -> backend.ceiling.Ceiling:
        if self.settings.test_mode:
            assert self.settings.camera_position is not None
            return backend.ceiling.Ceiling(
                type="test",
                rows=self.settings.rows,
                number_lights=self.settings.number_lights,
                dimensions=self.settings.dimensions,
                arrangement_file=self.settings.arrangement_file,
                number_children_for_division=self.settings.number_children_for_division,
                sphere_size=self.settings.sphere_size,
                camera_position=tuple(self.settings.camera_position),
                dimension_mask=self.settings.dimension_mask,
            )
        else:
            return Ceiling(
                type="ws281x",
                rows=self.settings.rows,
                number_lights=self.settings.number_lights,
                dimensions=self.settings.dimensions,
                arrangement_file=self.settings.arrangement_file,
                number_children_for_division=self.settings.number_children_for_division,
                io_pin=self.settings.io_pin,
                brightness=self.settings.brightness,
                pixel_order=self.settings.pixel_order,
                frequency=self.settings.frequency,
            )


global_state = State()
