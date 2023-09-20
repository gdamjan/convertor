# build stage
FROM python:3.11 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable --group web


# runtime image
FROM python:3.11-slim

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
            uwsgi-plugin-python3

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

COPY config/convertor.ini /srv/convertor.ini

ENTRYPOINT ["/usr/bin/uwsgi", "--ini=/srv/convertor.ini:docker"]
