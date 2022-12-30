#!/usr/bin/env python3

from typing import List, Union, Tuple, Any

from numpy._typing import NDArray
import numpy as np


RGB = Union[List[int], Tuple[int, int, int], NDArray[np.int32]]


def is_RGB(obj: Any) -> bool:
    if type(obj) is list:
        return len(obj) == 3
    elif type(obj) is tuple:
        return len(obj) == 3
    else:
        return False
