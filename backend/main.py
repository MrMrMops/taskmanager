import uvicorn
from fastapi import FastAPI, HTTPException, Depends


from api.endpoints.tasks import tasks_router

app = FastAPI()
app.include_router(tasks_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)