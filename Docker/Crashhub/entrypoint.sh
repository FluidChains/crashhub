#!/bin/sh

echo "Initializing database"
python3.6 -m flask init-db
if [ $? -eq 1 ]; then
    echo "Database failed to initialize"
fi

echo "Initializing uwsgi"
/root/.local/bin/uwsgi --http 0.0.0.0:5000 --processes 2 --threads 2 --master --wsgi-file crashhub.py --callable app
if [ $? -eq 1 ]; then
    echo "uwsgi failed to initialize"
fi