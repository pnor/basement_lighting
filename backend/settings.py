#!/usr/bin/env python3

"""
Parses configs from a toml file
"""

from typing import List, Optional
import toml


class Settings:
    def __init__(self, file_path: str):
        dict = toml.load(file_path)

        self.number_lights: int = dict["settings"]["number_lights"]
        self.arrangement_file: str = dict["settings"]["arrangement_file"]
        self.io_pin: int = dict["settings"]["io_pin"]
        self.dimensions: int = dict["settings"]["dimensions"]
        self.rows: Optional[List[int]] = dict["settings"].get("rows")

        self.sphere_size: Optional[float] = dict["test"].get("sphere_size")
        self.camera_position: Optional[List[float]] = dict["test"].get(
            "camera_position"
        )
        self.dimension_mask: Optional[List[int]] = dict["test"].get("dimension_mask")

        test_mode = dict["test"].get("test_mode")
        self.test_mode: bool = False if test_mode is None else bool(test_mode)
