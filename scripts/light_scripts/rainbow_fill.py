#!/usr/bin/env python3

# NAME: Rainbow Fill
# Fill all LEDs with changing colors based off the rainbow

import sys
from typing import Optional, Union
import colour

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb

from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        self.color = colour.Color(hsl=(0, 1, 0.5))
        super().__init__(interval * 5 if interval else 1)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self.color.set_hue(self.progress())
        ceil.fill(colour_rgb_to_neopixel_rgb(self.color.rgb))
        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    ceil = kwargs["ceiling"]
    ceil.clear()

    interval = kwargs.get("interval")
    interval = float(interval) if interval else None

    render_loop = Render(interval)
    render_loop.run(15, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True),
        interval=sys.argv[1] if len(sys.argv) > 1 else None,
    )
