#!/usr/bin/env python3

from typing import Callable, Union, Optional
from abc import ABC, abstractmethod
import time

from backend.ceiling import Ceiling
from backend.util import clamp

RenderLoop = Callable[[float, Ceiling], Union[bool, None]]


class RenderState(ABC):
    _cur: float = 0
    interval: Optional[float] = None

    @abstractmethod
    def __init__(self, interval: Optional[float]):
        """
        `interval`: keep track of how long until `interval` is reached.
        When `interval` is reacher, timer resets and `interval_reached` is called
        """
        self.interval = interval

    @abstractmethod
    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        pass

    def interval_reached(self, ceil: Ceiling) -> None:
        pass

    def run(self, FPS: float, ceil: Ceiling):
        """Handles boiler plate of running a render loop at `FPS` frames per second.

        `block` is a function (deltatime, ceiling) -> boolean that should be run
        every 1 / `FPS` seconds.

        If `block` returns False, the render loop will end. If `block` returns True (or nothing at all),
        will continue running in a loop
        """
        run = True
        delta = 1 / FPS
        while run is True or run is None:
            if self.interval is not None:
                self._cur += delta
                if self._cur > self.interval:
                    self._cur = 0
                    self.interval_reached(ceil)

            run = self.render(delta, ceil)
            time.sleep(delta)

    def progress(self) -> float:
        """Returns percetnage progress towards `_interval` (always 0..1)"""
        if self.interval is None:
            return 0
        else:
            return clamp(self._cur / self.interval, 0, 1)
