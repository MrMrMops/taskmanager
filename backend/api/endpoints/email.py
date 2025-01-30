from fastapi import APIRouter, BackgroundTasks
from api.tasks.email_task import send_email_task

email_router = APIRouter(prefix="/email",
                   tags=["email"])

@email_router.post("/send_email")
async def send_email(
    recipient: str, subject: str, body: str, background_tasks: BackgroundTasks
):
    """
    Отправить email в фоновом режиме через Celery.
    """
    send_email_task.delay(subject, body, recipient)
    return {"message": f"Email to {recipient} is being sent."}

