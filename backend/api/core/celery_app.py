from celery import Celery
from api.core.config import settings  # Импортируйте ваши настройки

celery_app = Celery(
    "taskmanager",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["api.tasks.email_task"],
)


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
)
