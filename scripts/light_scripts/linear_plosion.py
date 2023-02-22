#!/usr/bin/env python3

# NAME: Linear Plosions

import numpy as np
import sys
import colour
from typing import List, Optional, Union

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import (
    clamp,
    color_format_to_obj,
    color_obj_to_rgb,
    color_range,
    dim_color,
)
from scripts.library.render import RenderState


class Charger:
    pass


class Shockwave:
    pass


class Charger:
    def __init__(
        self, loc: int, color_obj: colour.Color, num_lights: int, speed: float
    ) -> None:
        self.loc = loc % num_lights
        self.CHARGE_TIME = 2 * (1 / speed)
        self.NUM_LIGHTS = num_lights
        self.cur_time = 0
        self.speed = speed

        self.color_obj = color_obj
        self.cur_color = color_obj_to_rgb(color_obj)
        # Chargin up to explode
        self.color_range = color_range(color_obj, colour.Color("white"), 50)
        # Fade into existence
        self.color_range = (
            color_range(dim_color(color_obj), color_obj, 10) + self.color_range
        )

    def step(self, delta: float, entity_list: List[Union[Charger, Shockwave]]):
        self.cur_time += delta
        prog: float = clamp(self.cur_time / self.CHARGE_TIME, 0, 0.999)

        color_from_range = self.color_range[int(prog * len(self.color_range))]
        self.cur_color = color_from_range

        shockwave_speed = self.speed * 30
        if self.cur_time > self.CHARGE_TIME:
            entity_list.append(
                Shockwave(self.loc, shockwave_speed, self.color_obj, self.NUM_LIGHTS)
            )
            entity_list.append(
                Shockwave(self.loc, -shockwave_speed, self.color_obj, self.NUM_LIGHTS)
            )

    def draw(self, ceil: Ceiling):
        ceil[int(self.loc)] = self.cur_color

    def is_dead(self) -> bool:
        return self.cur_time > self.CHARGE_TIME


class Shockwave:
    def __init__(
        self, loc: int, velocity: float, color_obj: colour.Color, num_lights: int
    ) -> None:
        self.loc = float(loc)
        self.velocity = velocity
        self.LIFETIME = 1
        self.NUM_LIGHTS = num_lights
        self.cur_time = 0
        self.color_range = color_range(color_obj, dim_color(color_obj), 50)
        self.cur_color = color_obj_to_rgb(color_obj)

    def step(self, delta: float, entity_list: List[Union[Charger, Shockwave]]):
        self.cur_time += delta

        self.loc += self.velocity * delta
        self.loc %= self.NUM_LIGHTS

        prog: float = clamp(self.cur_time / self.LIFETIME, 0, 0.999)
        color_from_range = self.color_range[int(prog * len(self.color_range))]
        self.cur_color = color_from_range

    def draw(self, ceil: Ceiling):
        # composit the color if it already has a color
        cur_color = ceil[int(self.loc) % self.NUM_LIGHTS]
        assert cur_color is not None
        cur_color = np.array(cur_color, dtype=np.int8)
        set_color = np.array(self.cur_color)
        new_color = cur_color + set_color
        new_color[0] = clamp(new_color[0], 0, 255)
        new_color[1] = clamp(new_color[1], 0, 255)
        new_color[2] = clamp(new_color[2], 0, 255)
        ceil[int(self.loc) % self.NUM_LIGHTS] = new_color

    def is_dead(self) -> bool:
        return self.cur_time > self.LIFETIME


def random_explosion(num_lights: int, color_obj: colour.Color, speed: float) -> Charger:
    return Charger(np.random.randint(num_lights - 1), color_obj, num_lights, speed)


class Render(RenderState):
    def __init__(
        self, color_obj: colour.Color, num_lights: int, interval: Optional[float]
    ):
        assert interval is not None

        self.speed = interval

        self.color_obj = color_obj
        self.entity_list: List[Union[Charger, Shockwave]] = [
            random_explosion(num_lights, color_obj, self.speed)
        ]
        super().__init__(0.3)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        for e in self.entity_list:
            e.step(delta, self.entity_list)

        for e in self.entity_list:
            e.draw(ceil)

        self.entity_list = list(filter(lambda e: not e.is_dead(), self.entity_list))

        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        if np.random.random() < 0.8:
            self.entity_list += [
                random_explosion(ceil.number_lights(), self.color_obj, self.speed)
            ]
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
