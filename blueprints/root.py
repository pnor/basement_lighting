from multiprocessing import Process
from typing import Callable, Optional
import threading
import importlib
import json
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

ls = [
    "Rainbow Pulsing",
    "Gaussian Noise + Flood",
    "All Black, Like OFF",
    "Sigmoid",
    "Fairy",
    "Snake",
    "Fire",
    "Water",
    "Party",
    "Strobe Fast",
    "Rainbow Perlin Noise",
    "Cloud",
]


class State:
    def __init__(self) -> None:
        self.current_process: Optional[Process] = None


state = State()


@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)


@bp.route("/start", methods=["POST"])
def start_script() -> str:
    data_dict = request.json
    print(data_dict)

    file_to_run = data_dict["file"]
    color = data_dict["color"]
    interval = data_dict["interval"]

    print(f"will run {file_to_run}")

    f = function_from_file(file_to_run)

    if state.current_process is not None:
        state.current_process.terminate()

    new_process = Process(target=f, args=(color, interval))
    state.current_process = new_process
    state.current_process.start()
    # TODO: capture stdout for debugging ?

    return json.dumps({"ok": True})


@bp.route("/stop", methods=["POST"])
def stop_script() -> str:
    if state.current_process:
        state.current_process.terminate()
    return json.dumps({"ok": True})


@bp.route("/state")
def get_state() -> str:
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


def function_wrapper(f: Callable) -> Callable[[str, float], None]:
    def _function_wrapper(color: str, interval: float):
        f(color=color, interval=interval)

    return _function_wrapper


def function_from_file(file: str) -> Callable:
    spec = importlib.util.spec_from_file_location("script_func", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return function_wrapper(mod.run)
