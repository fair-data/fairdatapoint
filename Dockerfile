FROM python:3-slim

RUN apt-get -y update && \
    apt-get -y install git make curl

RUN useradd fdp && \
    mkdir /home/fdp && \
    chown fdp:fdp /home/fdp

COPY . /home/fdp

WORKDIR /home/fdp

RUN pip install .
RUN pip install bottle paste

EXPOSE 8080

CMD ["/bin/bash", "fdp.sh"]

HEALTHCHECK --interval=5s CMD curl --silent --fail ${HOST_NAME}:${HOST_PORT} || exit 1