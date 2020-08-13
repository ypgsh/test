FROM python:3.6

MAINTAINER ypgsh <yangpeng@simright.com>

RUN apt-get update

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone

COPY . /app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl \
                          python-dev \
                          python-pip \
                          build-essential \
                          vim \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && pip install -i "https://pypi.douban.com/simple" -r requirements.txt
