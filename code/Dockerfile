FROM python:3.7-alpine3.9

ENV OJ_ENV production

ADD . /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python2 /app/deploy/health_check.py

RUN apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

RUN apk add git
RUN git clone https://github.com/rhsehfm33/Codeend.git /temp
RUN rm -rf /app/*
RUN cp -r /temp/code /app
RUN chmod 777 -R /app

ENTRYPOINT /app/deploy/entrypoint.sh
