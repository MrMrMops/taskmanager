import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from api.core.celery_app import celery_app
from api.endpoints.email import email_router
from api.endpoints.tasks import tasks_router
from api.endpoints.auth import auth_router


app = FastAPI()
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(email_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)