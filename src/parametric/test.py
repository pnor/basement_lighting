#!/usr/bin/env python3

import sys
import truecolor
import smartquadtree


class A:
    def __getitem__(self, key: slice) -> None:
        print(key.start)
        print(key.stop)

    def __setitem__(self, key: slice, value) -> None:
        print(key.start)
        print(key.stop)


a = A()
a[(1, 2):(3, 4)]

a = truecolor.fore_text(">>>", (255, 0, 11))
b = truecolor.fore_text(">>>", (134, 0, 11))
print(a + b)
