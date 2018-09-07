FROM alpine:3.8

COPY . /ick

RUN apk update && apk upgrade && apk add python=2.7.15-r1 py-pip imagemagick curl
RUN pip install --upgrade pip && pip install bs4==0.0.1 requests==2.19.1