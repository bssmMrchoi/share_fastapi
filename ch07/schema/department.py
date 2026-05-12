from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str
    personnel: int

class DepartmentResponse(DepartmentCreate):
    # DB 객체 -> json 변환
    model_config = ConfigDict(from_attributes=True)
    id: int