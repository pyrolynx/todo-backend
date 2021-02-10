from django.db import models
from typing import Optional
import pydantic


class ToDo(models.Model):
    task = models.CharField(max_length=256)
    complete = models.BooleanField(default=False)


class ToDoSchema(pydantic.BaseModel):
    id: Optional[int] = None
    task: str
    complete: bool = False
    
    class Config:
        orm_mode = True
