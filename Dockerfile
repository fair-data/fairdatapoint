FROM python:3-slim

RUN apt-get -y update && \
    apt-get -y install git make curl

RUN useradd fdp && \
    mkdir /home/fdp && \
    chown fdp:fdp /home/fdp

COPY . /home/fdp

WORKDIR /home/fdp

RUN pip install .

ENV HOST=0.0.0.0
ENV PORT=80

CMD fdp-run ${HOST} ${PORT}
HEALTHCHECK --interval=5s CMD curl --silent --fail ${HOST}:${PORT} || exit 1