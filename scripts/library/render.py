#!/usr/bin/env python3

from typing import Callable, Union, Optional
from abc import ABC, abstractmethod

from backend.ceiling import Ceiling

RenderLoop = Callable[[float, Ceiling], Union[bool, None]]


class RenderState(ABC):
    _cur: float = 0
    _interval: Optional[float] = None

    @abstractmethod
    def __init__(self, interval: float):
        """
        `interval`: keep track of how long until `interval` is reached.
        When `interval` is reacher, timer resets and `interval_reached` is called
        """
        self._interval = interval

    @abstractmethod
    def render(self, delta: float, ceiling: Ceiling) -> Union[bool, None]:
        pass

    def interval_reached(self, ceiling: Ceiling) -> None:
        pass

    def run(self, FPS: float, ceiling: Ceiling):
        """Handles boiler plate of running a render loop at `FPS` frames per second.

        `block` is a function (deltatime, ceiling) -> boolean that should be run
        every 1 / `FPS` seconds.

        If `block` returns False, the render loop will end. If `block` returns True (or nothing at all),
        will continue running in a loop
        """
        run = True
        delta = 1 / FPS
        while run is True or run is None:
            if self._interval is not None:
                self._cur += delta
                if self._cur > self._interval:
                    self._cur = 0
                    self.interval_reached(ceiling)

            run = self.render(delta, ceiling)

    def progress(self) -> float:
        """Returns percetnage progress towards `_interval`"""
        if self._interval is None:
            return 0
        else:
            return self._cur / self._interval
