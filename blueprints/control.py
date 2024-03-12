from multiprocess import Process
from typing import Callable, Optional
import importlib.util as importlib_util
import json
import numpy as np
import os
import random
import signal
import colour
import time
import logging, logging.handlers
from flask import Blueprint, request, current_app
from backend.ceiling_animation import circle_clear, circle_clear_soft, fade_out
from backend.constants import SCRIPT_LOGFILE_NAME, SCRIPT_LOGGER_NAME

from backend.state import global_state as state
from backend.ceiling import Ceiling
from backend.files import *

bp = Blueprint("control", __name__, url_prefix="/control")

# Transition Types
TRANSITION_START = "start"
TRANSITION_STOP = "start"
TRANSITION_COLOR_CHANGE = "color_change"


@bp.route("/start", methods=["POST"])
def start_script() -> str:
    """
    Runs the file provided in the request with the args color and interval
    """
    current_app.logger.info('Running "start script" route function')

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

    brightness = data_dict.get("brightness")
    brightness = int(brightness) if brightness else 120
    brightness = np.clip(brightness, 0, 255)

    current_app.logger.info(
        "Args: file_to_run: %s color: %s interval: %s brightness: %s",
        file_to_run,
        color,
        interval,
        brightness,
    )

    if not os.path.exists(file_to_run):
        current_app.logger.info("file '%s' does not exist!", file_to_run)
        return json.dumps(
            {"ok": False, "error": ("path doesn't exist: %s" % file_to_run)}
        )

    with state.lock:
        res = _start_script(file_to_run, color, interval, brightness, TRANSITION_START)

    if res:
        current_app.logger.info("succesfully started running script %s!", file_to_run)
        return json.dumps({"ok": True})
    else:
        current_app.logger.info(
            "crashed trying to load script %s as a module!!", file_to_run
        )
        return json.dumps(
            {
                "ok": False,
                "error": ("script %s crashed when loaded as a module", file_to_run),
            }
        )


@bp.route("/stop", methods=["POST"])
def stop_script() -> str:
    current_app.logger.info('Running "stop script" route function')

    with state.lock:
        _stop_script()

    return json.dumps({"ok": True})


@bp.route("/color", methods=["POST"])
def change_color() -> str:
    """
    Changes the color of the currently running script
    expects one arg for color
    """
    current_app.logger.info("Changing color of script")

    data_dict = request.json
    if data_dict is None:
        return json.dumps({"ok": False, "error": "request body requires color"})
    elif type(data_dict) is not dict:
        return json.dumps(
            {"ok": False, "error": "request body must contain json dictionary"}
        )

    color = data_dict.get("color")

    if color is None:
        current_app.logger.debug("Color was None so returning error json response")
        return json.dumps({"ok": False, "error": "request body requires arg for color"})

    with state.lock:
        current_app.logger.info("Changing color of script to %s", color)
        res = _change_color(color)

    if res:
        return json.dumps({"ok": True})
    else:
        return json.dumps(
            {
                "ok": False,
                "error": ("unable to change color to %s" % color),
            }
        )


def _start_script(
    path: str,
    color_arg: Optional[str],
    interval_arg: Optional[float],
    brightness: int,
    transition_type: str,
) -> bool:
    """Creates a new process to run the ceiling script.
    Returns True if it succesfully started the process."""
    # Stop running script
    if state.current_process is not None:
        state.current_process.terminate()
        state.current_process.join()

    # Update brightness
    state.settings.brightness = brightness

    # Load new script
    script = runnable_script(path, color_arg, interval_arg, transition_type)
    if script is None:
        print("Script crashed when loaded as a module")
        return False

    # Start new script
    state.current_process = script
    state.current_process.start()
    state.current_pattern = parse_script_name_from_file(path)

    state.current_script_path = path
    state.current_color = color_arg
    state.current_interval = interval_arg
    state.current_brightness = brightness

    return True


def _stop_script() -> None:
    """Stops currently running script, waiting for it to return the `Ceiling` object"""
    if state.current_process:
        state.current_process.terminate()
        state.current_process.join()
        state.current_process = None
        state.current_pattern = None

        state.current_script_path = None
        state.current_color = None
        state.current_interval = None
        state.current_brightness = None


def _change_color(color: str) -> bool:
    "Changes the color of the currently running script to `color`"

    if state.current_script_path is None:
        return True

    current_script_path = state.current_script_path
    current_interval = state.current_interval
    current_brightness = state.current_brightness
    _stop_script()
    return _start_script(
        current_script_path,
        color,
        current_interval,
        current_brightness,
        TRANSITION_COLOR_CHANGE,
    )


def function_wrapper(
    f: Callable, transition_type: str, logging_level: str
) -> Callable[[str, float], None]:
    """Wraps the function in another function that doesn't use keyword arguements.
    Also catches interrupts from `process.terminate()` to distinguish from actually crashing
    """

    def _exit_gracefully(sig_number, stack_frame):
        exit(0)

    def _function_wrapper(color: str, interval: float):
        signal.signal(signal.SIGTERM, _exit_gracefully)

        FORMAT = "%(asctime)-15s %(message)s"
        handler = logging.handlers.RotatingFileHandler(
            SCRIPT_LOGFILE_NAME, maxBytes=1024000, backupCount=3
        )
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[handler],
        )
        logging.getLogger(SCRIPT_LOGGER_NAME).setLevel(logging_level)

        try:
            now = int(time.time())
            np.random.seed(now)
            random.seed(now)
            ceiling = state.create_ceiling()
            if transition_type == TRANSITION_COLOR_CHANGE:
                fade_out(ceiling, 0.2)
            elif transition_type == TRANSITION_START:
                circle_clear_soft(ceiling, 0.8, colour.Color("white"))
            f(ceiling=ceiling, color=color, interval=interval)
        except Exception as e:
            print(e)
            exit(1)
        else:
            pass

    return _function_wrapper


def runnable_script(
    file: str,
    color_arg: Optional[str],
    interval_arg: Optional[float],
    transition_type: str,
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

    f = function_wrapper(mod.run, transition_type, "DEBUG")
    process = Process(
        target=f,
        args=(color_arg, interval_arg),
    )

    return process
