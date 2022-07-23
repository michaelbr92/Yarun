FROM python:3.9

ADD ./worker /app/
WORKDIR /app/

RUN echo "hello"
RUN pip install celery[redis] yara-python minio

CMD ["echo", "hello"]