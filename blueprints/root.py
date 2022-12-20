from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase
from typing import Callable, Optional, List, Tuple
import os
import importlib
import json
import signal
import threading
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from backend.ceiling import Ceiling
from backend.ceiling_animation import red_out
from backend.state import global_state as state

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)


@bp.route("/state")
def get_state() -> str:
    """ "
    Get the state of the currently running script.
    NOT_RUNNING: no script is running
    RUNNING: a script is correctly running
    GRACEFULLY_TERMINATED: the script ran and ended without crashing
    CRASHED: the script crashed
    """
    if state.current_process is None:
        return json.dumps({"state": "NOT_RUNNING"})

    exit_code = state.current_process.exitcode

    result = ""
    if exit_code is None:
        result = "RUNNING"
    elif exit_code == 0:
        result = "GRACEFULLY_TERMINATED"
    else:
        result = "CRASHED"

    return json.dumps({"state": result})


def get_scripts_and_names(dir: str) -> List[Tuple[str, str]]:
    """
    Parses files in `dir`  for runnable scripts. Returns (name, file_path)
    """
    base_name = dir + "/"

    skip_names = ["__init__.py"]

    files = os.listdir(base_name)
    files = [
        base_name + f
        for f in files
        if len(f) > 3 and f[-3:] == ".py" and f not in skip_names
    ]
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


# ========================================

paramaetric_name_and_script = get_scripts_and_names("parametric_scripts")
light_name_and_script = get_scripts_and_names("light_scripts")

ls = list(map(lambda t: t[0], paramaetric_name_and_script)) + list(
    map(lambda t: t[0], light_name_and_script)
)
