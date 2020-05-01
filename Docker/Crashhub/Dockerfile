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
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

COPY . /app

WORKDIR /app

RUN export PATH="$PATH:/root/.local/bin/"
RUN export PATH="$PATH:/usr/bin/python3.6"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN python3.6 -m pip install --user uwsgi
RUN python3.6 -m pip install --user -r requirements.txt

ENV APP_NAME $appName 
ENV GITHUB_PROJECT $githubProject
ENV GITHUB_TOKEN $githubToken
ENV POSTGRES_DB $postgresDatabase
ENV POSTGRES_USER $postgresUser
ENV POSTGRES_PASSWORD $postgresPassword

ENTRYPOINT exec /bin/sh entrypoint.sh