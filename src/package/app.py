from flask import Flask
import os
from package.blueprints import root
import sass
import sassutils
from sassutils.wsgi import SassMiddleware




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'package': ('static/sass', 'static/css', '/static/css')
    })

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
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

    return app
