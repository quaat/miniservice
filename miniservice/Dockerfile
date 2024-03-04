FROM python:3.11.8-slim as base

# Prevent writing .pyc files on the import of source modules
# and set unbuffered mode to ensure logging outputs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app


# Install requirements
COPY ./requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
