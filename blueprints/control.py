from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase
from typing import Callable, Optional, Tuple
import os
import importlib.util as importlib_util
import json
import signal
from flask import (
    Blueprint,
    request,
)
from backend.ceiling_animation import circle_clear
from backend.constants import SCRIPTS_PATH

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

    file_to_run = SCRIPTS_PATH + data_dict["file"]
    print(f"statt script running: {file_to_run}")
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
        state.ceiling.use_linear()
        state.recv_pipe = None

    recv_proc = file_to_pipe_and_runnable_script(path, color_arg, interval_arg)
    if not recv_proc:
        print("Script crashed when loaded as a module")
        return False

    recv, proc = recv_proc
    state.current_process = proc
    state.recv_pipe = recv
    state.current_process.start()
    state.current_pattern = parse_script_name_from_file(path)
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
        # With ceiling, animate clear
        circle_clear(state.ceiling, 0.2, (255, 255, 255))
        state.current_pattern = None


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

    def _prepare_to_exit():
        """Called when the normal script finishes"""
        ceiling.prepare_to_send()
        sender_pipe.send(ceiling)

    def _function_wrapper(color: str, interval: float):
        signal.signal(signal.SIGTERM, _exit_gracefully)
        try:
            circle_clear(ceiling, 0.2, (255, 255, 255))
            f(ceiling=ceiling, color=color, interval=interval)
        except Exception as e:
            print(e)
            _prepare_to_exit()
            exit(1)
        else:
            _prepare_to_exit()

    return _function_wrapper


def file_to_pipe_and_runnable_script(
    file: str, color_arg: Optional[str], interval_arg: Optional[int]
) -> Optional[Tuple[_ConnectionBase, Process]]:
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

    assert state.ceiling is not None
    receiver, sender = Pipe()
    f = function_wrapper(mod.run, state.ceiling, sender)
    process = Process(
        target=f,
        args=(color_arg, interval_arg),
    )

    return receiver, process
