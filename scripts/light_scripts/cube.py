#!/usr/bin/env python3

# NAME: Cube

# Based off of
# https://github.com/servetgulnaroglu/cube.c/blob/master/cube.c
# (computationally expensive to run, numba required)

import sys
from typing import Optional, Union
import numpy as np
from numpy._typing import NDArray
from numba import jit
from backend.backend_types import RGB
from backend.state import State

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb
from scripts.library.render import RenderState


width = 35
height = 15
distance_from_cam = 300
K1 = 40.0

increment_speed = 0.6

x, y, z = (0.0, 0.0, 0.0)
idx = 0


@jit(fastmath=True)
def calculate_x(i: int, j: int, k: int, A: float, B: float, C: float):
    return (
        (j * np.sin(A) * np.sin(B) * np.cos(C))
        - (k * np.cos(A) * np.sin(B) * np.cos(C))
        + (j * np.cos(A) * np.sin(C))
        + (k * np.sin(A) * np.sin(C))
        + (i * np.cos(B) * np.cos(C))
    )


@jit(fastmath=True)
def calculate_y(i: int, j: int, k: int, A: float, B: float, C: float):
    return (
        (j * np.cos(A) * np.cos(C))
        + (k * np.sin(A) * np.cos(C))
        - (j * np.sin(A) * np.sin(B) * np.sin(C))
        + (k * np.cos(A) * np.sin(B) * np.sin(C))
        - (i * np.cos(B) * np.sin(C))
    )


@jit(fastmath=True)
def calculate_z(i: int, j: int, k: int, A: float, B: float, C: float):
    return (k * np.cos(A) * np.cos(B)) - (j * np.sin(A) * np.cos(B)) + (i * np.sin(B))


@jit(fastmath=True)
def calculate_for_surface(
    cube_x: float,
    cube_y: float,
    cube_z: float,
    ch: int,
    horizontal_offset: float,
    A: float,
    B: float,
    C: float,
    buffer: NDArray[np.int8],
    zbuffer: NDArray[np.float64],
):
    x = calculate_x(int(cube_x), int(cube_y), int(cube_z), A, B, C)
    y = calculate_y(int(cube_x), int(cube_y), int(cube_z), A, B, C)
    z = calculate_z(int(cube_x), int(cube_y), int(cube_z), A, B, C) + distance_from_cam

    ooz = 1 / z

    xp = int(width / 2 + horizontal_offset + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)

    idx = xp + yp * width
    if idx >= 0 and idx < width * height:
        if ooz > zbuffer[idx]:
            zbuffer[idx] = ooz
            buffer[idx] = ch


@jit(fastmath=True)
def render_frame(
    A: float, B: float, C: float, buffer: NDArray[np.int8], zbuffer: NDArray[np.float64]
) -> NDArray[np.int8]:
    """Modifies buffer mutably"""
    zbuffer = np.zeros(width * height)
    buffer = np.zeros(width * height).astype(np.int8)

    cube_width = 30
    # horizontal_offset = -2 * cube_width
    horizontal_offset = 0
    # first cube
    for cube_x in np.arange(-cube_width, cube_width, increment_speed):
        for cube_y in np.arange(-cube_width, cube_width, increment_speed):
            calculate_for_surface(
                cube_x,
                cube_y,
                -cube_width,
                6,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )
            calculate_for_surface(
                cube_width,
                cube_y,
                cube_x,
                5,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )
            calculate_for_surface(
                -cube_width,
                cube_y,
                -cube_x,
                4,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )
            calculate_for_surface(
                -cube_x,
                cube_y,
                cube_width,
                3,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )
            calculate_for_surface(
                cube_x,
                -cube_width,
                -cube_y,
                2,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )
            calculate_for_surface(
                cube_x,
                cube_width,
                cube_y,
                1,
                horizontal_offset,
                A,
                B,
                C,
                buffer,
                zbuffer,
            )

    return buffer


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]) -> None:
        interval = interval if interval else 1
        self.color = np.array(color)

        self.zbuffer = np.zeros(160 * 44)
        self.buffer = np.zeros(160 * 44).astype(np.int8)

        self.A = 0
        self.B = 0
        self.C = 0

        super().__init__(interval * 0.5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        assert self.interval is not None

        self.buffer = render_frame(self.A, self.B, self.C, self.buffer, self.zbuffer)

        ceil.clear()
        for i in range(width * height):
            amt = float(self.buffer[i]) / 6
            col = (self.color * amt).astype(int)
            x_indx = (i % width) / width
            y_indx = (i / width) / height
            ceil[x_indx, y_indx] = col

        ceil.show()
        self.A += 0.05 * self.interval
        self.B += 0.05 * self.interval
        self.C += 0.01 * self.interval
        return super().render(delta, ceil)


def run(**kwargs):
    color = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.04)
    ceil.clear()

    render_loop = Render(color, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
