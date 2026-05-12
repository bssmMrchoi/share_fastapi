from fastapi import APIRouter, Depends

from ch07.db_connect import Session, get_db
from ch07.schema.student import StudentCreate, StudentResponse
from ch07.service import student as service

router = APIRouter(prefix="/student")

# 학생 등록에 대한 url과 메서
@router.post("", tags=["student"])
def create_student(data: StudentCreate, db: Session = Depends(get_db)) ->StudentResponse:
    return service.create(db, data)

@router.get("/dept/{dept_id}", response_model=list[StudentResponse])
def get_student_by_dept(dept_id: int, db: Session = Depends(get_db)):
    return service.get_by_dept_id(db, dept_id)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id:int, preferred_data: dict, db: Session = Depends(get_db)):
    return service.update_student(db, student_id, preferred_data)
