
from os import environ

from celery import Celery
from minio import Minio

broker_url = environ.get('BROKER_URL', 'redis://localhost:6379/0')
result_backend = environ.get('RESULT_BACKED', 'redis://localhost:6379/0')
minio_address = environ.get('MINIO_ADDRESS', 'localhost:9000')

celery_app = Celery('tasks',
                    broker=broker_url,
                    backend=result_backend,
                    include=["tasks"])

minio_client = Minio(
    minio_address,
    access_key="admin",
    secret_key="Password1!",
    secure=False
)
