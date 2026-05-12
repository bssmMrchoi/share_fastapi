from fastapi import APIRouter, Depends

from ch07.db_connect import Session, get_db
from ch07.schema.department import DepartmentResponse, DepartmentCreate, DepartmentUpdate
from ch07.schema.student import StudentResponse
from ch07.service import department as service
from ch07.service import student as student_service

router = APIRouter(prefix="/dept")

@router.post("", response_model=DepartmentResponse, status_code=201)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)) -> DepartmentResponse:
    return service.create(db, data)

@router.get("", response_model=list[DepartmentResponse])
def get_all_departments(db: Session = Depends(get_db)):
    return service.get_all(db)

@router.delete("/{id}") # /dept/3
def delete(db: Session = Depends(get_db), id: int = None) -> bool:
    return service.delete(db, id)

@router.get("/{dept_id}/students", response_model=list[StudentResponse])
def get_students_by_dept(dept_id: int, db: Session = Depends(get_db)):
    return service.get_students(db, dept_id)

@router.put("/{dept_id}", response_model=DepartmentResponse)
def update_dept(dept_id: int, data: DepartmentUpdate, db: Session = Depends(get_db)):
    return service.update_dept(db, dept_id, data)

@router.post("/assign")
def assign_department(db: Session = Depends(get_db)):
    return student_service.assign_dept(db)