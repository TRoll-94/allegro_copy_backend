FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apk add --update --no-cache python3 g++ make
RUN python -m pip install --upgrade pip
RUN apk update \
    && apk add postgresql-dev build-base \
    && apk add gettext
RUN apk add git
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
