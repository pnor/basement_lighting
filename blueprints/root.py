from multiprocessing import Process
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

bp = Blueprint("root", __name__, url_prefix="/")


class State:
    def __init__(self) -> None:
        self.current_process: Optional[Process] = None


state = State()


@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)


@bp.route("/start", methods=["POST"])
def start_script() -> str:
    """
    Runs the file provided in the request with the args color and interval
    """
    data_dict = request.json
    print(data_dict)

    file_to_run = data_dict["file"]
    color = data_dict.get("color")
    interval = data_dict.get("interval")

    print(f"will run {file_to_run}")

    f = function_from_file(file_to_run)

    if state.current_process is not None:
        state.current_process.terminate()

    new_process = Process(target=f, args=(color, interval))
    state.current_process = new_process
    state.current_process.start()
    return json.dumps({"ok": True})


@bp.route("/stop", methods=["POST"])
def stop_script() -> str:
    if state.current_process:
        state.current_process.terminate()
        state.current_process = None
    return json.dumps({"ok": True})


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


def function_wrapper(f: Callable) -> Callable[[str, float], None]:
    """Wraps the function in another function that doesn't use keyword arguements.
    Also catches interrupts from `process.terminate()` to distinguish from actually crashing
    """

    def _exit_gracefully():
        exit(0)

    def _function_wrapper(color: str, interval: float):
        signal.signal(signal.SIGTERM, _exit_gracefully)
        f(color=color, interval=interval)

    return _function_wrapper


def function_from_file(file: str) -> Callable:
    """
    Converts a path to a file to a function that can be called in this runtime
    Function in the file should be called "run(**kwargs)"
    """
    spec = importlib.util.spec_from_file_location("script_func", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return function_wrapper(mod.run)


# ========================================

paramaetric_name_and_script = get_scripts_and_names("parametric_scripts")
light_name_and_script = get_scripts_and_names("light_scripts")

ls = list(map(lambda t: t[0], paramaetric_name_and_script)) + list(
    map(lambda t: t[0], light_name_and_script)
)
