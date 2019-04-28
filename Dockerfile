FROM alpine:3.9

COPY . /ick

RUN apk update && apk upgrade && apk add python3
RUN pip3 install --upgrade pip
RUN pip3 install -r /ick/requirements.txt