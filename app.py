from flask import Flask

import os
import logging

from backend.constants import APP_LOGFILE
from blueprints import root, control


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    FORMAT = "%(asctime)-15s %(message)s"
    handler = logging.handlers.RotatingFileHandler(
        APP_LOGFILE, maxBytes=1024000, backupCount=3
    )
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler],
    )
    app.logger.setLevel("DEBUG")

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    app.register_blueprint(root.bp)
    app.register_blueprint(control.bp)

    return app
