FROM python:3.6-stretch

ENV HOST=0.0.0.0
ENV PORT=8080

RUN apt-get update -y && \
    apt-get install git make curl -y

RUN useradd lta && \
    mkdir /home/lta && \
    chown lta:lta /home/lta

COPY fdp-api/python /home/lta

WORKDIR /home/lta

RUN make install

EXPOSE ${PORT}

CMD python -m bottle -b ${HOST}:${PORT} fdp

HEALTHCHECK --interval=5s CMD curl --silent --fail ${HOST}:${PORT} || exit 1
