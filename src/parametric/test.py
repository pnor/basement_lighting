#!/usr/bin/env python3

import sys
import truecolor
import smartquadtree
from blessings import Terminal
import time


class A:
    def __getitem__(self, key: slice) -> None:
        print(key.start)
        print(key.stop)

    def __setitem__(self, key: slice, value) -> None:
        print(key.start)
        print(key.stop)


a = A()
a[(1, 2):(3, 4)]

t = Terminal()
a = truecolor.fore_text(">>>", (255, 0, 11))
b = truecolor.fore_text(">>>", (134, 0, 11))
print(a + b)
print(a + b)
print(a + b)
time.sleep(0.3)
# t.move(3, 1)

a = truecolor.fore_text("<<<", (255, 0, 11))
b = truecolor.fore_text("<<<", (134, 0, 11))
print((t.move_up * 3) + a + b)
print(a + b)
print(a + b)
