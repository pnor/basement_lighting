#!/usr/bin/env python3

# NAME: Convolutions

import numpy as np
import sys
import copy
import colour
from typing import Optional, Union

from numpy._typing import NDArray
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_obj, color_range, dim_color, mix_colors_fast
from scripts.library.render import RenderState


def convolve_pixel(image_subsection, filter) -> float:
    return np.clip(np.sum(np.multiply(image_subsection, filter)), 0, 1 - (10 ** (-6)))


def random_kernel(size) -> NDArray:
    def _beta() -> NDArray:
        filter = np.random.beta(0.5, 0.5, (size, size))
        filter = filter / np.sum(filter)
        return filter

    def _binom() -> NDArray:
        filter = np.random.binomial(size, 1 / size, (size, size))
        filter = filter / np.sum(filter)
        return filter

    def _unsharp() -> NDArray:
        axs = np.linspace(-(size - 1) / 2, (size - 1) / 2, size)
        gauss = np.exp(-0.5 * np.square(axs) / np.square(1))
        blur = np.outer(gauss, gauss)
        filter = np.zeros((size, size))
        filter[size // 2, size // 2] = 1
        filter = filter - blur
        return filter

    def _shift():
        filter = np.zeros((size, size))
        filter[np.random.randint(size), np.random.randint(size)] = 1
        return filter

    def _DoG():
        axs = np.linspace(-(size - 1) / 2, (size - 1) / 2, size)
        gauss_a = np.exp(-0.5 * np.square(axs) / np.square(5))
        gauss_b = np.exp(-0.5 * np.square(axs) / np.square(25))
        gauss_a = np.outer(gauss_a, gauss_a)
        gauss_b = np.outer(gauss_b, gauss_b)
        return gauss_b - gauss_a

    funcs = [_beta, _binom, _unsharp, _shift, _DoG]
    f = np.random.choice(funcs)
    return f()


class Render(RenderState):
    def __init__(
        self,
        color: colour.Color,
        num_lights: int,
        interval: Optional[float],
        ceil: Ceiling,
    ):
        assert interval is not None
        self.SIDE_LENGTH = 10
        self.FILTER_SIDE_LENGTH = 3

        color1 = copy.deepcopy(color)
        color2 = copy.deepcopy(color)
        color2.hue = (color2.hue + 0.12) % 1
        color3 = copy.deepcopy(color)
        color3.hue = (color3.hue + 0.3) % 1
        color3.luminance = 0.01

        self.colors = color_range(color1, color2, 20)
        self.colors += color_range(color2, color3, 10)

        self.base_grid = np.zeros(self.SIDE_LENGTH)
        self.base_grid[::2] = 1
        self.base_grid[1::2] = 0
        self.base_grid = np.outer(self.base_grid, self.base_grid)
        self.base_grid = np.pad(
            self.base_grid, pad_width=self.FILTER_SIDE_LENGTH // 2, constant_values=1
        )

        self.next_grid = self.base_grid
        self.filter = random_kernel(self.FILTER_SIDE_LENGTH)

        super().__init__(interval * 1)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        index = int(self.progress() * (self.SIDE_LENGTH**2))
        pad_size = self.FILTER_SIDE_LENGTH // 2

        row = index // self.SIDE_LENGTH
        col = index % self.SIDE_LENGTH

        x = row + pad_size
        y = col + pad_size

        x_low = x - pad_size
        x_high = x + pad_size + 1
        y_low = y - pad_size
        y_high = y + pad_size + 1

        prog = convolve_pixel(self.base_grid[x_low:x_high, y_low:y_high], self.filter)
        self.next_grid[x, y] = prog

        ceil.clear()
        for i in range(self.SIDE_LENGTH**2):
            row = i // self.SIDE_LENGTH
            col = i % self.SIDE_LENGTH
            pad_size = self.FILTER_SIDE_LENGTH // 2
            prog = np.clip(
                self.next_grid[pad_size:-pad_size][row, col], 0, 1 - (10 ** (-6))
            )
            color = self.colors[int(prog * len(self.colors))]
            ceil[row / self.SIDE_LENGTH, col / self.SIDE_LENGTH] = color

        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.base_grid = self.next_grid
        self.filter = random_kernel(self.FILTER_SIDE_LENGTH)
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.1)
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval, ceil)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True, print_to_stdout=True),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
