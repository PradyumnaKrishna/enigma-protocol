FROM ubuntu:20.04

COPY . /app
WORKDIR /app

RUN apt update && apt install -y python3 python3-pip
RUN pip install --upgrade -r requirements.txt

CMD /bin/bash start_app.sh
