FROM python:2.7-alpine3.7

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY . .

RUN apk add --no-cache --virtual .build-deps autoconf gcc g++ make libffi-dev openssl-dev && \
    pip install -r requirements.txt && \
    apk del .build-deps

CMD python sync.py