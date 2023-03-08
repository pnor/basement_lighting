import json
from flask import (
    Blueprint,
    render_template,
    request,
)

from backend.state import global_state as state
from backend.files import *

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls, url=state.settings.url)


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
    pattern = "N/A"
    if exit_code is None:
        result = "RUNNING"
        pattern = state.current_pattern
    elif exit_code == 0:
        result = "GRACEFULLY_TERMINATED"
        pattern = state.current_pattern
    else:
        result = "CRASHED"
        pattern = state.current_pattern

    return json.dumps({"state": result, "pattern": pattern})


@bp.route("/brightness", methods=["POST"])
def set_brightness() -> str:
    """
    Sets max brightness of light
    """
    data_dict = request.json
    if data_dict is None or data_dict.get("brightness") is None:
        return json.dumps(
            {"ok": False, "error": "request body requires brightness: int key pair"}
        )

    try:
        brightness = int(data_dict["brightness"])
    except ValueError:
        return json.dumps({"ok": False, "error": "brightness could not be parsed"})

    if brightness not in range(256):
        return json.dumps({"ok": False, "error": "brightness must be 0..255"})

    with state.lock:
        state.settings.brightness = brightness

    return json.dumps({"ok": True})


# ========================================

script_names = get_scripts_and_names("scripts/light_scripts")

ls = script_names
