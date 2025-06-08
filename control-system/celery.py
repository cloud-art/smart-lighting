from celery import Celery
from core.config import settings

app = Celery("tasks", broker=settings.CELERY_BROKER_URL)
