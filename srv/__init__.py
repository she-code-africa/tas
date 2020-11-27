import os

from flask import Flask

from srv import root, file
from config import config


def create_app(config_name=None) -> Flask:
    """Create and configure an instance of the Flask application."""

    env_app_settings = config_name
    if not config_name:
        try:
            env_app_settings = os.environ['APP_SETTINGS']
        except:
            env_app_settings = 'production'

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[env_app_settings])

    app.register_blueprint(root.bp)
    app.register_blueprint(file.bp)
    return app


app = create_app()
