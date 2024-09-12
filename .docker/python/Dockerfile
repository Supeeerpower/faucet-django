FROM python:3.12.1-bullseye

ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PASS
ARG DB_PORT
ARG WALLET_ADDRESS
ARG PRIVATE_KEY
ARG PIP_DEFAULT_TIMEOUT

ENV DB_HOST=$DB_HOST \
    DB_NAME=$DB_NAME \
    DB_USER=$DB_USER \
    DB_PASS=$DB_PASS \
    DB_PORT=$DB_PORT \
    WALLET_ADDRESS=$WALLET_ADDRESS \
    PRIVATE_KEY=$PRIVATE_KEY \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=$PIP_DEFAULT_TIMEOUT \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app
COPY . /app/

COPY requirements.txt ./app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./app/requirements.txt
RUN mkdir -p /var/www/static
VOLUME /var/www/static
VOLUME /app/config/media

COPY ./.shell/entrypoint.sh /app/.shell/entrypoint.sh
RUN chmod +x /app/.shell/entrypoint.sh
ENTRYPOINT ["/app/.shell/entrypoint.sh"]