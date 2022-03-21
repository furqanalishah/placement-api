from apiflask import APIFlask
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy

from config import flask_config

compress = Compress()
db = SQLAlchemy()


def create_app(environment):
    app = APIFlask(__name__, title="Placement API Docs", version="1.0", redoc_path="/apidocs")
    config = flask_config[environment]
    app.config.from_object(config)
    app.logger.setLevel(config.LOGGING_LEVEL_MAPPED)
    compress.init_app(app)
    db.init_app(app)
    db.app = app

    from .buckets import buckets as buckets_blueprint

    app.register_blueprint(buckets_blueprint, urlprefix="/api")

    return app
