from fastapi import APIRouter, Depends

from ch07.db_connect import Session, get_db
from ch07.schema.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/student")

# 학생 등록에 대한 url과 메서
@router.post("", tags=["student"])
def create_student(data: StudentCreate, db: Session = Depends(get_db)) ->StudentResponse:
    return service.create(db, data)


