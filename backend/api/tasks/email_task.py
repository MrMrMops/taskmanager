import smtplib
from email.message import EmailMessage
from aiosmtplib import send
from api.core.config import settings
from api.core.celery_app import celery_app
from celery import shared_task

@celery_app.task
def send_email_task(subject: str, body: str, recipient: str):
    """
    Синхронная задача Celery для отправки email.
    """
    email = EmailMessage()
    email["From"] = settings.SMTP_USER
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(body)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(email)
            print(email)
        return f"Email sent to {recipient}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"