FROM python:3.6-stretch

RUN apt-get update -y && apt-get install git make -y

# Service user
RUN useradd fdp && mkdir /home/fdp && chown fdp:fdp /home/fdp

COPY fdp-api/python /home/fdp

WORKDIR /home/fdp

RUN make install

EXPOSE 8080

CMD python -m bottle -b 0.0.0.0:8080 fdp
