from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, UUID4, constr

class TaskCreate(BaseModel):
    title: constr(min_length=1, max_length=255) = Field(..., description="Title of the task")
    text: str | None = Field(None, description="Detailed description of the task")
    image_url: HttpUrl | None = Field(None, description="URL of the task's related image")
    due_date: datetime | None = Field(
        None,
        description="Deadline for the task",
        example="2025-01-20T15:00:00"
    )
    priority: int = Field(
        1,
        ge=1,
        le=5,
        description="Priority of the task (1-5, where 1 is highest priority)"
    )
class Task(TaskCreate):
    id: UUID4
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the task was created")
    updated_at: datetime | None = Field(None, description="Timestamp when the task was last updated")

    class Config:
        schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "text": "Document all APIs before the deadline",
                "image_url": "https://example.com/image.png",
                "due_date": "2025-01-20T15:00:00",
                "priority": 2,
                "created_at": "2025-01-01T10:00:00"
            }
        }


