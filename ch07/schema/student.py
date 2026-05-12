from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from ch07.model.student import Gender


class StudentCreate(BaseModel):
    name: str
    gender: Gender
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    department_id: int
    preferred_department_id: Optional[int] = None

class StudentResponse(StudentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int