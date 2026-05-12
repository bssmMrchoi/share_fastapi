from fastapi import HTTPException

from ch07.data import department as data
from ch07.db_connect import Session
from ch07.schema.department import DepartmentCreate, DepartmentResponse
from ch07.schema.student import StudentResponse


def create(db: Session, department: DepartmentCreate) -> DepartmentResponse:
    # 학과 이름 중복 확인
    existing_department = data.find_by_name(db, department.name)
    if existing_department:
        raise HTTPException(status_code=409,
                            detail=f"학과 이름이 이미 존재합니다. {department.name}")
    dept = data.insert(db, department.name, department.personnel)
    return DepartmentResponse.model_validate(dept)

def get_all(db: Session):
    departments = data.find_all(db)
    return [DepartmentResponse.model_validate(d) for d in departments]


def delete(db: Session, id: int) -> bool:

    dept = data.find_by_id(db, id)

    # 1. 학과가 존재하는가?
    if dept is None:
        raise HTTPException(status_code=404,
                            detail=f"학과가 존재하지 않습니다. 학과 id = {id}")
    # 학과 존재함
    # 2. 소속된 학생들이 있는가?
    if dept.students:
        raise HTTPException(status_code=409,
                            detail=f"소속학생이 있어 삭제할 수 없습니다. 학생: {len(dept.students)}")
    else:
        data.delete(db, id)
        return True


def get_students(db: Session, dept_id: int):
    dept = data.find_by_id(db, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="존재하지 않는 학과입니다.")
    # s = dept.students
    return [StudentResponse.model_validate(s) for s in dept.students]






