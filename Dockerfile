FROM python:3.11.7 AS builder

ENV LANG en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN pip3 install --upgrade pip && \
    pip3 install PyGithub && \
    pip3 install slack_bolt

ADD ./src /src

ENTRYPOINT ["/usr/local/bin/python3", "/src/run.py"]
