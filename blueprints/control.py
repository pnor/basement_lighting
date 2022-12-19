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

from backend.state import global_state as state

bp = Blueprint("control", __name__, url_prefix="/control")

@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)


@bp.route("/start", methods=["POST"])
def start_script() -> str:
    """
    Runs the file provided in the request with the args color and interval
    """
    data_dict = request.json

    file_to_run = data_dict["file"]
    color = data_dict.get("color")
    interval = data_dict.get("interval")

    if not os.path.exists(file_to_run):
        return json.dumps(
            {"ok": False, "error": ("path doesn't exist: %s" % file_to_run)}
        )

    res = _start_script(file_to_run, color, interval)
    if res:
        return json.dumps({"ok": True})
    else:
        return json.dumps(
            {
                "ok": False,
                "error": ("script %s crashed when loaded as a module" % file_to_run),
            }
        )


@bp.route("/stop", methods=["POST"])
def stop_script() -> str:
    _stop_script()
    return json.dumps({"ok": True})


def _start_script(
    path: str, color_arg: Optional[str], interval_arg: Optional[int]
) -> bool:
    """Hands off `state.ceiling` to the new script.
    Returns True if it succesfully started the process."""
    if state.current_process is not None:
        state.current_process.terminate()
        assert state.recv_pipe is not None
        assert state.ceiling is None
        state.ceiling = state.recv_pipe.recv()
        state.recv_pipe = None

    recv_proc = file_to_pipe_and_runnable_script(path, color_arg, interval_arg)
    if not recv_proc:
        print("Script crashed when loaded as a module")
        return False

    recv, proc = recv_proc
    state.current_process = proc
    state.recv_pipe = recv
    state.current_process.start()
    # Relinquish control of the ceiling to the running script
    state.ceiling = None

    return True

def _stop_script() -> None:
    """Stops currently running script, waiting for it to return the `Ceiling` object"""
    if state.current_process:
        assert state.recv_pipe is not None
        state.current_process.terminate()
        state.ceiling = state.recv_pipe.recv()
        assert state.ceiling is not None
        state.current_process = None
        state.recv_pipe = None

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
