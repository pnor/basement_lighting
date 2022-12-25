#!/usr/bin/env python3

from typing import List, Union, Tuple, Any


RGB = Union[List[int], Tuple[int, int, int]]


def is_RGB(obj: Any) -> bool:
    if type(obj) is list:
        return len(obj) == 3
    elif type(obj) is tuple:
        return len(obj) == 3
    else:
        return False
