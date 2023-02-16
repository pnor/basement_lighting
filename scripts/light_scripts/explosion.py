#!/usr/bin/env python3

# NAME: Explosion

import numpy as np
import sys
import copy
import colour
from typing import List, Optional, Union

from numpy._typing import NDArray

from backend.ceiling import Ceiling
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
        self,
        pos: NDArray[np.float32],
        color_obj: colour.Color,
        speed: float,
    ) -> None:
        self.pos = pos
        self.RADIUS = 0.2

        self.CHARGE_TIME = 5 * (1 / speed)
        self.cur_time = 0
        self.speed = speed

        self.color_obj = color_obj
        self.cur_color = color_obj_to_rgb(color_obj)
        # Chargin up to explode
        self.color_range = color_range(color_obj, colour.Color("white"), 200)
        # Fade into existence
        self.color_range = (
            color_range(dim_color(color_obj), color_obj, 25) + self.color_range
        )

    def step(self, delta: float, entity_list: List[Union[Charger, Shockwave]]):
        self.cur_time += delta
        prog: float = clamp(self.cur_time / self.CHARGE_TIME, 0, 0.999)

        color_from_range = self.color_range[int(prog * len(self.color_range))]
        self.cur_color = color_from_range

        if self.cur_time > self.CHARGE_TIME:
            for i in np.linspace(0, 2 * np.pi, 50):
                shockwave_speed = (self.speed * 1.0) + (
                    np.random.random() * (self.speed * 2)
                )
                shockwave_accel = -(np.random.random() * (self.speed * 1))

                if np.random.random() < 0.7:
                    s = Shockwave(
                        np.array([0.0, i]),
                        shockwave_speed,
                        shockwave_accel,
                        self.color_obj,
                    )
                    entity_list.append(s)

    def draw(self, ceil: Ceiling):
        ceil[self.pos[0], self.pos[1], self.RADIUS] = self.cur_color

    def is_dead(self) -> bool:
        return self.cur_time > self.CHARGE_TIME


class Shockwave:
    def __init__(
        self,
        r_theta: NDArray[np.float32],
        r_velocity: float,
        r_accel: float,
        base_color_obj: colour.Color,
    ) -> None:
        self.r_theta = r_theta
        self.r_velocity = r_velocity
        self.r_accel = r_accel

        self.cur_time = 0
        self.LIFETIME = 2

        color_obj = copy.deepcopy(base_color_obj)
        color_obj.hue = clamp(color_obj.hue + (np.random.random() * 0.1 - 0.05), 0, 1)
        color_obj.luminance = clamp(
            color_obj.hue + (np.random.random() * 0.5 - 0.25), 0, 1
        )
        self.color_range = color_range(color_obj, dim_color(color_obj), 20)

    def step(self, delta: float, entity_list: List[Union[Charger, Shockwave]]):
        self.cur_time += delta
        prog: float = clamp(self.cur_time / self.LIFETIME, 0, 0.999)

        self.r_theta[0] += self.r_velocity * delta
        self.r_velocity += self.r_accel * delta

        color_from_range = self.color_range[int(prog * len(self.color_range))]
        self.cur_color = color_from_range

    def draw(self, ceil: Ceiling):
        ceil[self.r_theta[0], self.r_theta[1]] = self.cur_color

    def is_dead(self) -> bool:
        return self.cur_time > self.LIFETIME


def random_explosion(num_lights: int, color_obj: colour.Color, speed: float) -> Charger:
    return Charger(np.array([0.5, 0.5]), color_obj, speed)


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
        super().__init__(interval * 10)

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
        self.entity_list += [
            random_explosion(ceil.number_lights(), self.color_obj, self.speed)
        ]
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_polar((0.5, 0.5))
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
