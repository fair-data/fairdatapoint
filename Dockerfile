FROM python:3.6-slim

ENV HOST=0.0.0.0
ENV PORT=8080

RUN apt-get update -y && \
    apt-get install git make curl -y

RUN useradd fdp && \
    mkdir /home/fdp && \
    chown fdp:fdp /home/fdp

COPY . /home/fdp

RUN mkdir /home/fdp/data
COPY samples/minimal.ttl /home/fdp/data/config.ttl

WORKDIR /home/fdp

RUN pip install .

EXPOSE ${PORT}

CMD fdp-run /home/fdp/data/config.ttl

HEALTHCHECK --interval=5s CMD curl --silent --fail ${HOST}:${PORT} || exit 1
