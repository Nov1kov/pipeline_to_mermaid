FROM python:3-slim

ARG project_version
ENV PROJECT_VERSION=$project_version

WORKDIR /usr/src/app

COPY ./ ./
RUN pip install --no-cache-dir . && \
    rm -rf *