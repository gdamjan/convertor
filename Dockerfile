FROM debian:buster-slim AS builder

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
        python3-setuptools python3-wheel python3-pip

# copy all to /src and install there into PYTHONUSERBASE
ENV PYTHONUSERBASE=/srv/convertor
COPY . /src
RUN pip3 install --user /src/[web]

# Runtime
FROM debian:buster-slim
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
            uwsgi-plugin-python3

ENV PYTHONUSERBASE=/srv/convertor
COPY --from=builder /srv/convertor /srv/convertor
COPY config/convertor.ini /srv/convertor.ini

ENTRYPOINT ["/usr/bin/uwsgi", "--ini=/srv/convertor.ini:docker"]
