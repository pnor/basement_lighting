#!/usr/bin/env python3

# from ..src.backend.led_locations import LEDSpace
from byronsbasement import *
from backend.led_locations import LEDSpace

# from byronsbasement.backend.led_locations import LEDSpace
import pytest


def test_led_space_simple_zigzag():
    led_space = LEDSpace()
