from multiprocessing import Process
from typing import Callable, Optional
import importlib.util as importlib_util
import json
import numpy as np
import os
import random
import signal
import time
from flask import (
    Blueprint,
    request,
)
from flask_socketio import send, emit, socketio

from backend.ceiling_animation import circle_clear, row_clear
from backend.state import global_state as state
from backend.ceiling import Ceiling
from backend.files import *

bp = Blueprint("control", __name__, url_prefix="/control")


@bp.route("/start", methods=["POST"])
def start_script() -> str:
    """
    Runs the file provided in the request with the args color and interval
    """
    data_dict = request.json
    if data_dict is None:
        return json.dumps(
            {"ok": False, "error": "request body requires path to script to start"}
        )
    elif type(data_dict) is not dict:
        return json.dumps(
            {"ok": False, "error": "request body must contain json dictionary"}
        )

    file_to_run = data_dict["file"]

    color = data_dict.get("color")

    interval = data_dict.get("interval")
    interval = float(interval) if interval else None

    if not os.path.exists(file_to_run):
        return json.dumps(
            {"ok": False, "error": ("path doesn't exist: %s" % file_to_run)}
        )

    with state.lock:
        res = _start_script(file_to_run, color, interval)

    if res:
        emit("get_state", {"data": "RUNNING"}, namespace="/", broadcast=True)
        return json.dumps({"ok": True})
    else:
        emit("get_state", {"data": "CRASHED"}, namespace="/", broadcast=True)
        return json.dumps(
            {
                "ok": False,
                "error": ("script %s crashed when loaded as a module" % file_to_run),
            }
        )


@bp.route("/stop", methods=["POST"])
def stop_script() -> str:
    with state.lock:
        _stop_script()
    emit("get_state", {"data": "STOPPED"}, namespace="/", broadcast=True)
    return json.dumps({"ok": True})


def _start_script(
    path: str, color_arg: Optional[str], interval_arg: Optional[float]
) -> bool:
    """Creates a new process to run the ceiling script.
    Returns True if it succesfully started the process."""
    # Stop running script
    if state.current_process is not None:
        state.current_process.terminate()
        state.current_process.join()

    # Load new script
    script = runnable_script(path, color_arg, interval_arg)
    if script is None:
        print("Script crashed when loaded as a module")
        return False

    # Start new script
    state.current_process = script
    state.current_process.start()
    state.current_pattern = parse_script_name_from_file(path)

    return True


def _stop_script() -> None:
    """Stops currently running script, waiting for it to return the `Ceiling` object"""
    if state.current_process:
        state.current_process.terminate()
        state.current_process.join()
        state.current_process = None
        state.current_pattern = None


def function_wrapper(f: Callable) -> Callable[[str, float], None]:
    """Wraps the function in another function that doesn't use keyword arguements.
    Also catches interrupts from `process.terminate()` to distinguish from actually crashing
    """

    def _exit_gracefully(sig_number, stack_frame):
        # Send back the ceiling to the main app
        emit(
            "get_state",
            {"data": "GRACEFULLY_TERMINATED"},
            namespace="/",
            broadcast=True,
        )
        exit(0)

    def _function_wrapper(color: str, interval: float):
        signal.signal(signal.SIGTERM, _exit_gracefully)
        try:
            now = int(time.time())
            np.random.seed(now)
            random.seed(now)
            ceiling = state.create_ceiling()
            circle_clear(ceiling, 0.2, np.array((255, 255, 255)))
            f(ceiling=ceiling, color=color, interval=interval)
        except Exception as e:
            print(e)
            exit(1)
        else:
            pass

    return _function_wrapper


def runnable_script(
    file: str, color_arg: Optional[str], interval_arg: Optional[float]
) -> Optional[Process]:
    """
    Converts a path to a file to a process containing the function
    Function in the file should be called "run(**kwargs)"

    Also wraps the function in code that will pass the ceiling between the script process and this process
    """
    spec = importlib_util.spec_from_file_location("script_func", file)
    if spec is None:
        return None

    mod = importlib_util.module_from_spec(spec)

    spec_loader = spec.loader
    if spec_loader is None:
        return None

    try:
        spec_loader.exec_module(mod)
    except:  # Script fails to execute
        return None

    f = function_wrapper(mod.run)
    process = Process(
        target=f,
        args=(color_arg, interval_arg),
    )

    return process
