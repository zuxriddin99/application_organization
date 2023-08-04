FROM python:3.9.6-buster

ENV PROJECT_PATH=/usr/src/application_organization

RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH
RUN mkdir -p $PROJECT_PATH/static
RUN mkdir -p $PROJECT_PATH/media

COPY . .

ENV VIRTUAL_ENV=/usr/src/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 netcat supervisor nano

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000