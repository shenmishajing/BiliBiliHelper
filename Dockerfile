FROM python:3.6-alpine

MAINTAINER shenmishajing <shenmishajing@gmail.com>

ENV BILIBILI_USER="" \
    BILIBILI_PASSWORD=""

WORKDIR /app

RUN apk add --no-cache git python3-dev py-pip build-base
RUN git clone https://github.com/TheWanderingCoel/BiliBiliHelper.git /app
RUN pip install -r requirements.txt

CMD sed -i ''"$(cat Conf/Account.conf -n | grep "BILIBILI_USER =" | awk '{print $1}')"'c '"$(echo "BILIBILI_USER = ${BILIBILI_USER}")"'' Conf/Account.conf && \
    sed -i ''"$(cat Conf/Account.conf -n | grep "BILIBILI_PASSWORD =" | awk '{print $1}')"'c '"$(echo "BILIBILI_PASSWORD = ${BILIBILI_PASSWORD}")"'' Conf/Account.conf && \
    python ./main.py
