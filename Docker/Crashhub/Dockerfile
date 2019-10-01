FROM ubuntu:16.04

ARG appName
ARG githubProject
ARG githubToken
ARG dbEngine
ARG dbHost
ARG dbPort
ARG postgresUser
ARG postgresPassword
ARG postgresDatabase

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

COPY . /app

ENV APP_NAME $appName 
ENV GITHUB_PROJ $githubProject
ENV GITHUB_TOKEN $githubToken
ENV DB_ENGINE $dbEngine
ENV DB_NAME $postgresDatabase
ENV DB_HOST $dbHost
ENV DB_PORT $dbPort
ENV DB_USER $postgresUser
ENV DB_PASS $postgresPassword

WORKDIR /app

RUN pip3 install --user -r requirements.txt

WORKDIR /app/src

RUN pip3 install uwsgi PyMySQL psycopg2-binary

#RUN python3 setup.py install

CMD uwsgi --http localhost:8081 --processes 2 --threads 2 --master --wsgi-file crashhub.py --callable app
