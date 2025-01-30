from celery import Celery
from api.core.config import settings  # Импортируйте ваши настройки

celery_app = Celery(
    "taskmanager",
    broker=settings.CELERY_BROKER_URL,  # Пример: "redis://localhost:6379/0"
    backend=settings.CELERY_RESULT_BACKEND,  # Пример: "redis://localhost:6379/0"
    include=["api.tasks.email_task"],  # Укажите путь к модулю с задачами
)

# Настройки Celery
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
)
