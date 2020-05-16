# pull official base image
FROM python:3.8-apine

# set work directory
RUN mkdir /app
WORKDIR /app

# set environment variables
# Impede que o Python grave arquivos pyc no disco
ENV PYTHONDONTWRITEBYTECODE 1
# Impede que o Python armazene em buffer stdout e stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev && apkpip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh

# copy project
COPY . /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]