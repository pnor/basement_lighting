#!/usr/bin/env python3

"""
Parses configs from a toml file
"""

from typing import List, Optional, Tuple
import toml
import csv


class Settings:
    def __init__(self, file_path: str):
        dict = toml.load(file_path)

        # url
        self.url: str = dict["settings"]["url"]

        # arrangement file, number lights + dimensions
        self.arrangement_file: str = dict["settings"]["arrangement_file"]
        dimensions, number_lights = preprocess_arrangement_file(self.arrangement_file)

        # Number children for division
        number_children_for_division = None
        performance_section = dict.get("performance")
        if performance_section:
            number_children_for_division = performance_section.get(
                "number_children_for_division"
            )
        if number_children_for_division is None:
            self.number_children_for_division = 10
        else:
            self.number_children_for_division = number_children_for_division

        # Number lights
        num_lights = dict["settings"].get("number_lights")
        self.number_lights: int = (
            num_lights if num_lights is not None else number_lights
        )

        # Dimensions
        dims = dict["settings"].get("dimensions")
        self.dimensions: int = dims if dims is not None else dimensions

        # io pin
        self.io_pin: int = dict["settings"]["io_pin"]

        # brightness
        brightness: int = dict["settings"].get("brightness")
        self.brightness: int = brightness if brightness else 255

        # pixel order
        pixel_order: str = dict["settings"].get("pixel_order")
        self.pixel_order: str = pixel_order if pixel_order else "rgb"

        # frequency
        frequency: int = dict["settings"].get("frequency")
        self.frequency: int = frequency if frequency else 800000

        # rows
        self.rows: Optional[List[int]] = dict["settings"].get("rows")

        # sphere size
        self.sphere_size: Optional[float] = dict["test"].get("sphere_size")
        self.camera_position: Optional[List[float]] = dict["test"].get(
            "camera_position"
        )

        # dimension mask
        self.dimension_mask: Optional[List[int]] = dict["test"].get("dimension_mask")

        # test mode
        test_mode = dict["test"].get("test_mode")
        self.test_mode: bool = False if test_mode is None else bool(test_mode)


def preprocess_arrangement_file(file: str) -> Tuple[int, int]:
    """
    Infers the number of lights and total number of dimensions from the arrangement csv file

    Witht this, you acn omit number_lights and dimensions
    """
    num_lines = sum(1 for line in open(file) if line.strip() != "")

    first_row = True
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if first_row:
                first_row = False
            else:
                dimensions = len(row) - 1
                return dimensions, num_lines - 1

    raise Exception("Failed to preprocess arrangement file!")
