FROM python:3.6-stretch

RUN apt-get update -y && apt-get install git make -y

# Service user
RUN useradd lta && mkdir /home/lta && chown lta:lta /home/lta

COPY fdp-api/python /home/lta

WORKDIR /home/lta

RUN make install

EXPOSE 8080

CMD python -m bottle -b 0.0.0.0:8080 fdp
