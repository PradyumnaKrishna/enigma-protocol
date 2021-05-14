FROM python:3.8-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add g++
RUN pip install --upgrade -r requirements.txt

CMD python main.py
