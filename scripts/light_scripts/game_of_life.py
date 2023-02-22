#!/usr/bin/env python3

# NAME: Game of Life
# Using code from
# http://drsfenner.org/blog/2015/08/game-of-life-in-numpy-2/
# which implements it taking advantage of numpy

import sys
from typing import Optional, Union
import numpy as np
from numpy._typing import NDArray
from numba import jit
from backend.backend_types import RGB
import colour

from backend.ceiling import Ceiling
from backend.ceiling_animation import circle_clear
from backend.state import State
from backend.util import color_format_to_rgb, color_obj_to_rgb
from scripts.library.render import RenderState


from numpy.lib.stride_tricks import as_strided

# board dimensions
BOARD_HEIGHT = 7
BOARD_WIDTH = 30


def grid_nD(arr):
    assert all(_len > 2 for _len in arr.shape)

    nDims = len(arr.shape)
    newShape = [_len - 2 for _len in arr.shape]
    newShape.extend([3] * nDims)

    newStrides = arr.strides + arr.strides

    return as_strided(arr, shape=newShape, strides=newStrides)


# index is number of neighbors alive
ruleOfLifeAlive = np.zeros(8 + 1, np.uint8)  # default all to dead
ruleOfLifeAlive[[2, 3]] = 1  # alive stays alive <=> 2 or 3 neighbors

ruleOfLifeDead = np.zeros(8 + 1, np.uint8)  # default all to dead
ruleOfLifeDead[3] = 1  # dead switches to living <=> 3 neighbors


class GameOfLife(object):
    def __init__(self, board_size=(10, 10)):
        full_size = tuple(i + 2 for i in board_size)
        self.full = np.zeros(full_size, dtype=np.uint8)
        nd_slice = (slice(1, -1),) * len(board_size)
        # self.board = self.full[1:-1,1:-1,...]
        self.board = self.full[nd_slice]
        self.ndims = len(self.board.shape)

    def run_board(self, N_ITERS=10):
        for i in range(N_ITERS):
            neighborhoods = grid_nD(self.full)
            # shape = (10,10) --> (-1, -2)
            sumOver = tuple(-(i + 1) for i in range(self.ndims))
            neighborCt = np.sum(neighborhoods, sumOver) - self.board
            self.board[:] = np.where(
                self.board, ruleOfLifeAlive[neighborCt], ruleOfLifeDead[neighborCt]
            )


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        interval = interval if interval else 1
        self.game = GameOfLife(board_size=(BOARD_HEIGHT, BOARD_WIDTH))
        self.color_obj = colour.Color(hsl=(0, 1, 0.5))
        self.cur_iter = 0
        self.MAX_ITERATIONS = 200

        # prepopulate the board
        self.reset_board()

        super().__init__(interval)

    def reset_board(self):
        self.game.board *= 0
        for i in range(75 + int(np.random.random() * 60)):
            y = int(np.random.random() * BOARD_WIDTH)
            x = int(np.random.random() * BOARD_HEIGHT)
            self.game.board[x, y] = 1

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.game.run_board(N_ITERS=1)

        ceil.clear()

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                x = i / BOARD_HEIGHT
                x += 1 / (BOARD_HEIGHT * 2)

                y = j / BOARD_WIDTH
                y += 1 / (BOARD_WIDTH * 2)

                col = (
                    color_obj_to_rgb(self.color_obj)
                    if self.game.board[i, j] == 1
                    else (0, 0, 0)
                )
                ceil[x, y] = col
        ceil.show()

        self.color_obj.hue = (self.color_obj.hue + 0.02) % 1
        self.cur_iter += 1
        if self.cur_iter > self.MAX_ITERATIONS or np.sum(self.game.board) == 0:
            self.cur_iter = 0
            self.reset_board()
            circle_clear(ceil, 0.5, color_obj_to_rgb(self.color_obj))
        return super().interval_reached(ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.04)
    ceil.clear()

    render_loop = Render(interval / 2)
    render_loop.run(5, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        interval=sys.argv[1],
    )
