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
from backend.files import *;

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
    pattern = "N/A"

    result = ""
    if exit_code is None:
        result = "RUNNING"
        pattern = state.current_pattern
    elif exit_code == 0:
        result = "GRACEFULLY_TERMINATED"
    else:
        result = "CRASHED"
        pattern = state.current_pattern

    return json.dumps({"state": result, "pattern": pattern})

# ========================================

parametric_name_and_script = get_scripts_and_names("parametric_scripts")
light_name_and_script = get_scripts_and_names("light_scripts")

ls = parametric_name_and_script + light_name_and_script
