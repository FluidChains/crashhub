# crashhub.py

from Crashhub import create_app

app = create_app()

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, threaded=True, use_reloader=False)