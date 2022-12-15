#!/usr/bin/env python3


class A:
    def __getitem__(self, key: slice) -> None:
        print(key.start)
        print(key.stop)

    def __setitem__(self, key: slice, value) -> None:
        print(key.start)
        print(key.stop)


a = A()
a[(1, 2):(3, 4)]
