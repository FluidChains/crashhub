FROM python:3
LABEL maintainer="Johann Bauer <bauerj@bauerj.eu>"

RUN pip3 install uwsgi PyMySQL psycopg2-binary

COPY . /app

WORKDIR /app

RUN pip3 install --user -r requirements.txt

CMD uwsgi --socket localhost:8081 --processes 2 --threads 2 --master --wsgi-file /app/crashhub.py --callable app
