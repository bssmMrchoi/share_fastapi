from fastapi import HTTPException

from ch07.db_connect import Session
from ch07.schema.student import StudentResponse, StudentCreate
from ch07.data import department as dept_data


def create(db: Session, student: StudentCreate) -> StudentResponse:
    # 1. 학과(department_id)의 존재 유무
    # 2. 신청한 학과(preferred_department_id)의 존재 유무
    dept = dept_data.find_by_id(db, student.department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    if student.preferred_department_id:
        preferred = dept_data.find_by_id(db, student.preferred_department_id)
        if not preferred:
            raise HTTPException(status_code=404, detail="Preferred department not found")
    s = student_data.create(db, student.name, student.gender, student.score,
                        student.department_id, student.preferred_department_id)
    return StudentResponse.model_validate(s)