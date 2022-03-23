import logging
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class PaginationConfig:
    DEFAULT_ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 50


class MYSQLConfig:
    MYSQL_PARAMS = {
        "MYSQL_USER": os.environ.get("MYSQL_USER", "root"),
        "MYSQL_PASSWORD": os.environ.get("MYSQL_PASSWORD", "admin123"),
        "MYSQL_HOST": os.environ.get("MYSQL_HOST", "placement_db"),
        "MYSQL_PORT": os.environ.get("MYSQL_PORT", "3306"),
        "MYSQL_DATABASE": os.environ.get("MYSQL_DATABASE", "placement_db")
    }

    MYSQLDB_URL = "mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}".format(
        **MYSQL_PARAMS
    )


class SQLAlchemyConfig:
    SQLALCHEMY_DATABASE_URI = MYSQLConfig.MYSQLDB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", "400"))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", "450"))
    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", "5"))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", "0"))
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
        "pool_timeout": SQLALCHEMY_POOL_TIMEOUT,
        "pool_size": SQLALCHEMY_POOL_SIZE,
        "max_overflow": SQLALCHEMY_MAX_OVERFLOW
    }


class FlaskConfig:
    __LOGGING_LEVEL_MAPPER = {
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    try:
        LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
        LOGGING_LEVEL_MAPPED = __LOGGING_LEVEL_MAPPER[LOGGING_LEVEL]
    except KeyError:
        raise ValueError(f"LOGGING_LEVEL should be one of {list(__LOGGING_LEVEL_MAPPER.keys())}")

    SECRET_KEY = os.environ.get("SECRET_KEY", "my_precious_aws")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAX_CONTENT_LENGTH = 2048 * 2048


class FlaskDevelopmentConfig(FlaskConfig, SQLAlchemyConfig):
    # Flask Configs
    DEBUG = True
    USE_SSL = os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Port is not a flask env variable but is used in a custom logic to set the port for the flask server
    PORT = 8081


flask_config = {
    "development": FlaskDevelopmentConfig,
    "default": FlaskDevelopmentConfig,
}
