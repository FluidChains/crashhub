#!/bin/python3

from flask import Flask
from lib.routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
