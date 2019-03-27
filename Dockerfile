FROM python:3.6-stretch

ENV HOST=0.0.0.0
ENV PORT=8080

RUN apt-get update -y && \
    apt-get install git make curl -y

RUN useradd fdp && \
    mkdir /home/fdp && \
    chown fdp:fdp /home/fdp

COPY fdp-api/python /home/fdp

WORKDIR /home/fdp

RUN make install

EXPOSE ${PORT}

# TODO: change this to run from bin
CMD python -m bottle -b ${HOST}:${PORT} fdp

HEALTHCHECK --interval=5s CMD curl --silent --fail ${HOST}:${PORT} || exit 1
