#!/usr/bin/env python3

# NAME: render example

from typing import Optional, Union
from backend.ceiling import Ceiling
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        # initialize state used across render frames here
        self.index_to_set = 0
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        # Update the display every frame
        ceil.clear(False)
        color = [255, 255, 255]
        # progress returns % towards the next interval
        color[self.index_to_set] = int(self.progress() * color[self.index_to_set])
        ceil[0] = color
        ceil.show()
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        # This function is run every `interval` seconds
        self.index_to_set = (self.index_to_set + 1) % 3
        return super().interval_reached(ceil)


def run(**kwargs):
    ceil: Ceiling = kwargs["ceiling"]
    ceil.clear()

    # start the render loop
    render_loop = Render(1)
    render_loop.run(FPS=30, ceil=ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling())
