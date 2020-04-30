# Crashhub/views/__init__.py
from flask import Blueprint

bp_crash = Blueprint('bp_crash', __name__)

from . import crash