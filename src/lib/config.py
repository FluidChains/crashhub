import json
import signal
import os

config = {}


def read_config(*_):
    global config
    config = {
        "app_name": os.environ['APP_NAME'],
        "github_project": os.environ['GITHUB_PROJ'],
        "github_token": os.environ['GITHUB_TOKEN'],
        "db_engine": os.environ['DB_ENGINE'],
        "db_name": os.environ['DB_NAME'],
        "db_host": os.environ['DB_HOST'],
        "db_port": os.environ['DB_PORT'],
        "db_user": os.environ['DB_USER'],
        "db_password": os.environ['DB_PASS']
    }


def get(key, default=None):
    if key in config:
        return config[key]
    if default:
        return default
    raise MissingValueError(key)


class MissingValueError(BaseException):
    pass

try:
    # Reload config when SIGHUP is sent
    signal.signal(signal.SIGHUP, read_config)
except AttributeError:
    pass  # Windows
read_config()
