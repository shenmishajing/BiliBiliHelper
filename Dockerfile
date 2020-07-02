FROM python:3.6-alpine

MAINTAINER shenmishajing <shenmishajing@gmail.com>

ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=0

WORKDIR /app

RUN apk add --no-cache tzdata libressl-dev libffi-dev build-base git python3-dev py-pip
RUN git clone https://github.com/shenmishajing/BiliBiliHelper.git /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python ./main.py -d
