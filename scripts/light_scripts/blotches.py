#!/usr/bin/env python3

# NAME: Blotches

import sys
import colour
from typing import List, Optional, Tuple, Union
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, color_obj_to_rgb, color_range, dim_color
from scripts.library.render import RenderState
from backend.ceiling_animation import circle_clear, fade_out


def blotch_locations(num_blotches: int) -> List[Tuple[float, float]]:
    edge_length = int(np.sqrt(num_blotches))
    bump = 1 / (edge_length * 2)

    res = []
    for i in range(edge_length):
        for j in range(edge_length):
            x = (i / edge_length) + bump
            y = (j / edge_length) + bump
            res += [(x, y)]
    return res


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        super().__init__(interval)
        self.BLOTCHES = 64  # sqrt of this number should be an integer
        assert abs(np.sqrt(self.BLOTCHES) - int(np.sqrt(self.BLOTCHES))) < 0.01

        random_hue = np.random.random()
        self.color = colour.Color(hsl=(random_hue, 1, 0.5))
        self.locations = blotch_locations(self.BLOTCHES)
        np.random.shuffle(self.locations)
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        if len(self.locations) > 0:
            x, y = self.locations.pop(0)
            ceil[x, y] = color_obj_to_rgb(self.color)
            ceil.show()
        else:
            if np.random.random() < 0.1:
                circle_clear(ceil, 0.2, color_obj_to_rgb(self.color))
            else:
                fade_out(ceil, 0.2, color_obj_to_rgb(self.color))
            random_hue = np.random.random()
            self.color = colour.Color(hsl=(random_hue, 1, 0.5))

            self.locations = blotch_locations(self.BLOTCHES)
            np.random.shuffle(self.locations)

        return super().interval_reached(ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(interval / 3)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True),
        interval=sys.argv[1],
    )
