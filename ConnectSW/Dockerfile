# pull official base image
FROM python:3.7

# set work directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pipenv

# install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD gunicorn ConnectSW.wsgi -b 0.0.0.0:8000

# BUILD IMAGE
# docker-compose up --build -d

# Comando Milagroso
# docker system prune -a -f
