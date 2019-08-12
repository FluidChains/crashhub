FROM python:3
LABEL maintainer="Johann Bauer <bauerj@bauerj.eu>"

RUN pip install uwsgi PyMySQL psycopg2-binary
RUN useradd crashhub

COPY . /app

RUN python /app/setup.py install

USER crashhub

WORKDIR /app

CMD uwsgi --socket localhost:8081 --processes 2 --threads 2 --master --wsgi-file /app/crashhub.py --callable app
