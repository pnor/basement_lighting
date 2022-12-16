from typing import Callable
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


@bp.route("/")
def route_main():
    return render_template("index.html", patterns=ls)


@bp.route("/start")
def start_script():
    data = request.data
    data_dict = json.load(data)

    file_to_run = data_dict["file"]
    color = data_dict["color"]
    interval = data_dict["interval"]

    f = function_from_file(file_to_run)
    f(color, interval)


@bp.route("/stop")
def stop_script():
    pass


@bp.route("/state")
def get_state():
    pass


def function_from_file(file: str) -> Callable:
    spec = importlib.util.spec_from_file_location("script_func", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run
