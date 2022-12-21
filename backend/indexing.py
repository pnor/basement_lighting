#!/usr/bin/env python3

from typing import Any, Optional

from backend.backend_types import RGB


"""
Abstraction of how indexing gets and sets indeces
"""


class Indexing:
    """
    Abstract class representing how getting indeces and setting indeces operate
    """

    def __init__(self):
        pass

    def get(self, key: Any) -> Optional[RGB]:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")

    def set(self, key: Any, newvalue: RGB) -> None:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")

    def prepare_to_send(self):
        """Function called to prepare indexing objects to be pickled if they are using objects that
        do not handle pickling well.

        One primary example is the quadtree object
        """
        raise NotImplementedError("'Indexing' class is abstract and should not be used")
