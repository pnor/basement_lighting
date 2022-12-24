import os
from typing import Callable, Optional, List, Tuple

from backend.constants import SCRIPTS_PATH


def get_scripts_and_names(dir: str) -> List[Tuple[str, str]]:
    """
    Parses files in `dir`  for runnable scripts. Returns (name, file_path)
    """
    skip_names = ["__init__.py"]

    files = os.listdir(dir)
    files = [f for f in files if len(f) > 3 and f[-3:] == ".py" and f not in skip_names]
    names = [parse_script_name_from_file(f) for f in files]
    return list(zip(names, files))


def parse_script_name_from_file(path) -> str:
    """Parses `path` for the name of the script
    The name should be formatted:
    # NAME: <name of script>
    in a docstring towards the top of the file
    """
    SEARCH_STR = "# NAME:"
    with open(path) as file:
        for line in file.readlines():
            indx = line.find(SEARCH_STR)
            if indx == 0:
                return line[len(SEARCH_STR) :].strip()
    return path
