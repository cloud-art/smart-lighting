from celery import Celery
import os

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

celery_app = Celery('tasks', broker=CELERY_BROKER_URL)
