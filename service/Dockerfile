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


################# DEVELOPMENT ####################################
FROM base as development
COPY . .

# Run static security check and linters
#RUN pylint app

# Run with reload option
CMD uvicorn asgi:app --reload --host 0.0.0.0 --port 5000
EXPOSE 5000


################# PRODUCTION ####################################
FROM base as production
COPY . .

# Run app
#CMD hypercorn asgi:app --bind 0.0.0.0:80
CMD uvicorn asgi:app --host 0.0.0.0 --port 80
EXPOSE 80