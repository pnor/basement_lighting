#!/usr/bin/env python3

from typing import List, Optional, Tuple, Union

from backend.backend_types import RGB

# import backend.ceiling
from backend.coordinate_conversions import polar


class Ceiling:
    pass


def linear_getitem(key: int, ceiling: Ceiling) -> RGB:
    return ceiling.get_by_index(key % ceiling.number_lights())


def linear_setitem(key: Union[int, slice], color: RGB, ceiling: Ceiling):
    if type(key) is slice:
        start = key.start if key.start else 0
        stop = key.stop if key.stop else ceiling.number_lights()
        step = key.step if key.step else 1
        for i in range(start, stop, step):
            ceiling.set_by_index(i % ceiling.number_lights(), color)
    else:
        ceiling.set_by_index(key % ceiling.number_lights(), color)


def row_getitem(key: Tuple[int, int], ceiling: Ceiling) -> RGB:
    """key: (row, col)"""
    row, col = key
    index = row_col_to_indx(row, col, ceiling)
    return ceiling.get_by_index(index)


def row_setitem(key: Union[Tuple[int, int], int], color: RGB, ceiling: Ceiling) -> None:
    """
    key: (row, col) or row
    if key is a tuple, will set one LED. If key is an int corresponding to the row, will set
    every LED in the row
    """
    if type(key) is tuple and len(key) == 2:
        row, col = key
        index = row_col_to_indx(row, col, ceiling)
        ceiling.set_by_index(index, color)
    elif type(key) is int:
        row = key
        for i in range(ceiling.rows()[row]):
            index = row_col_to_indx(row, i, ceiling)
            ceiling.set_by_index(index, color)
    else:
        raise NotImplementedError("key for row indexing was neither tuple or int")


def row_col_to_indx(row: int, col: int, ceiling: Ceiling) -> int:
    """Convert row and col position to index in light strip"""
    if ceiling.rows() is None:
        raise ValueError("Ceiling has no rows!")

    rows = ceiling.rows()
    assert rows is not None

    row = row % len(rows)
    indx = sum(rows[:row])
    if row % 2 == 0:
        indx += col
    else:
        indx += rows[row] - col
    return indx


def cartesian_getitem(
    key: Tuple[float, float], search_radius: float, ceiling: Ceiling
) -> Optional[RGB]:
    """key: (x, y), x and y in (0..1)"""
    x, y = key
    return ceiling.get_closest([x, y], search_radius)


def cartesian_setitem(
    key: Union[Tuple[float, float], slice],
    color: RGB,
    ceiling: Ceiling,
) -> None:
    """key: either a tuple or slice.
    If tuple, (x, y) are in (0..1)
    If slice, is 2 tuples, (x1, y1):(x2, y2), and will set box spanning x1..x2 and y1..y2 to
    same color"""
    if type(key) is slice:  # box
        x1, y1 = key.start
        x2, y2 = key.stop
        ceiling.set_all_in_box([x1, y1], [x2, y2], color)
    else:
        x, y = key
        ceiling.set_closest(
            [x, y],
            ceiling._search_radius,
            color,
        )


def flaot_cartesian_getitem(key: List[float], ceiling: Ceiling) -> Optional[RGB]:
    """key: (x, y), x and y in (0..1)"""
    return ceiling.get_closest(key, ceiling._search_radius)


def float_cartesian_setitem(
    key: Union[List[float], slice],
    color: RGB,
    ceiling: Ceiling,
) -> None:
    """key: either a tuple or slice.
    If tuple, (x, y) are in (0..1)
    If slice, is 2 tuples, (x1, y1):(x2, y2), and will set box spanning x1..x2 and y1..y2 to
    same color"""
    if type(key) is slice:  # box
        x1, y1 = key.start
        x2, y2 = key.stop
        ceiling.set_all_in_box([x1, y1], [x2, y2], color)
    else:
        loc = key
        ceiling.set_decreasing_intensity_merge(
            loc,
            ceiling._set_radius,
            color,
        )


def polar_getitem(
    key: Tuple[float, float],
    ceiling: Ceiling,
) -> Optional[RGB]:
    """
    key: (radius, theta)
    """
    r, theta = key
    loc = polar(r, [theta], ceiling._center)
    return ceiling.get_closest(loc, ceiling._search_radius)


def polar_setitem(
    key: Union[Tuple[float, float, float], Tuple[float, float]],
    color: RGB,
    ceiling: Ceiling,
) -> None:
    """
    key: either a tuple of 2 or 3 elements.
    If tuple of 2, represents (r, theta)
    If tuple of 3, represetns (x, y, r) and will fill a circle of radius `r` centered at `(x,
    y)` with `newvalue`. When doing this, `(x, y)` ignore origin, and are based in (0..1, 0..1)
    """
    if len(key) == 3:
        x, y, r = key
        ceiling.set_all_in_radius([x, y], r, color)
    else:
        r, theta = key
        loc = polar(r, [theta], ceiling._center)
        ceiling.set_closest(loc, ceiling._set_radius, color)


def float_polar_getitem(
    key: Tuple[float, float],
    ceiling: Ceiling,
) -> Optional[RGB]:
    """
    key: (radius, theta)
    """
    r, theta = key
    loc = polar(r, [theta], ceiling._center)
    return ceiling.get_closest(loc, ceiling._search_radius)


def float_polar_setitem(
    key: Union[Tuple[float, float, float], Tuple[float, float]],
    color: RGB,
    ceiling: Ceiling,
) -> None:
    """
    key: either a tuple of 2 or 3 elements.
    If tuple of 2, represents (r, theta)
    If tuple of 3, represetns (x, y, r) and will fill a circle of radius `r` centered at `(x,
    y)` with `newvalue`. When doing this, `(x, y)` ignore origin, and are based in (0..1, 0..1)
    """
    if len(key) == 3:
        x, y, r = key
        ceiling.set_all_in_radius([x, y], r, color)
    else:
        r, theta = key
        loc = polar(r, [theta], ceiling._center)
        ceiling.set_decreasing_intensity_merge(loc, ceiling._set_radius, color)
