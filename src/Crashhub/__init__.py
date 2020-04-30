# Crashhub/__init__.py
import os

from flask import Flask, jsonify

from flask_cors import CORS

from .views import bp_crash 
from .db import db
from .lib.github import gh_crash as github

def create_app():

    # Logging

    # Flask App
    app = Flask(__name__, instance_relative_config=True, static_url_path=None)

    # Default route
    @app.route('/')
    def root():
        return jsonify({'msg': 'Crashhub'}), 200

    # Blueprints
    # v1
    app.register_blueprint(bp_crash)

    # Config
    if os.environ["FLASK_ENV"] == 'development':
        app.config.from_pyfile('config.py')
    else:
        app.config.from_object('config.ProductionConfig')

    # CORS
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    
    # Db
    db.init_app(app)

    # Github
    github.init_app(app)

    # Log Level

    return app
