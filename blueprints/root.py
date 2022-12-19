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


def function_wrapper(
    f: Callable, ceiling: Ceiling, sender_pipe: _ConnectionBase
) -> Callable[[str, float], None]:
    """Wraps the function in another function that doesn't use keyword arguements.
    Also catches interrupts from `process.terminate()` to distinguish from actually crashing
    """

    def _exit_gracefully(sig_number, stack_frame):
        # Send back the ceiling to the main app
        ceiling.prepare_to_send()
        sender_pipe.send(ceiling)
        exit(0)

    def _exit_normally():
        """Called when the normal script finishes"""
        ceiling.prepare_to_send()
        sender_pipe.send(ceiling)

    def _function_wrapper(color: str, interval: float):
        signal.signal(signal.SIGTERM, _exit_gracefully)
        try:
            f(ceiling=ceiling, color=color, interval=interval)
        except:
            _exit_normally()
        else:
            _exit_normally()

    return _function_wrapper


def file_to_pipe_and_runnable_script(
    file: str, color_arg: Optional[str], interval_arg: Optional[int]
) -> Optional[Tuple[_ConnectionBase, Process]]:
    """
    Converts a path to a file to a process containing the function
    Function in the file should be called "run(**kwargs)"

    Also wraps the function in code that will pass the ceiling between the script process and this process
    """
    spec = importlib.util.spec_from_file_location("script_func", file)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except:  # Script fails to execute
        return None

    assert state.ceiling is not None
    receiver, sender = Pipe()
    f = function_wrapper(mod.run, state.ceiling, sender)
    process = Process(
        target=f,
        args=(color_arg, interval_arg),
    )

    return receiver, process


# ========================================

paramaetric_name_and_script = get_scripts_and_names("parametric_scripts")
light_name_and_script = get_scripts_and_names("light_scripts")

ls = list(map(lambda t: t[0], paramaetric_name_and_script)) + list(
    map(lambda t: t[0], light_name_and_script)
)
