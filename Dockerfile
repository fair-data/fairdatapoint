FROM python:3-slim

RUN apt-get -y update && \
    apt-get -y install git make curl && \
    useradd fdp && \
    mkdir /home/fdp && \
    chown fdp:fdp /home/fdp

COPY . /home/fdp

WORKDIR /home/fdp

RUN pip install . && \
    pip install gunicorn

ENV FDP_HOST=0.0.0.0
ENV FDP_PORT=80
EXPOSE 80

CMD fdp-run ${FDP_HOST} ${FDP_PORT}