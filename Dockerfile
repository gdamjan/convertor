ARG PY=3.11
# build stage
FROM python:${PY} AS builder
ARG PY

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable --group web
RUN mv /project/__pypackages__/$PY/lib /project/pkgs
RUN mv /project/__pypackages__/$PY/bin /project/bin

# runtime image
FROM python:${PY}-slim

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/pkgs /project/pkgs

# retrieve executables
COPY --from=builder /project/bin/* /usr/bin/

ENV PORT=8000
ENTRYPOINT ["gunicorn", "convertor.web_app:application"]
