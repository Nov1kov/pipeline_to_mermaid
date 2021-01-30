FROM python:3-slim

WORKDIR /usr/src/app

COPY ./ ./
RUN pip install --no-cache-dir .