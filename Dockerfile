FROM ubuntu:16.04

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

WORKDIR /app

RUN pip3 install uwsgi PyMySQL psycopg2-binary
RUN pip3 install --user -r requirements.txt

RUN python3 /app/setup.py install

CMD uwsgi --socket localhost:8081 --processes 2 --threads 2 --master --wsgi-file /app/crashhub.py --callable app
