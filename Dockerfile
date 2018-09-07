FROM alpine:3.8

COPY . /imgchap

RUN apk update && apk upgrade && apk add python=2.7.15-r1 py-pip imagemagick
RUN pip install --upgrade pip && pip install bs4 requests
RUN /imgchap/imgchap.sh

CMD /bin/sh