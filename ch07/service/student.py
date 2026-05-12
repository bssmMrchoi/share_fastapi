from typing import List

from fastapi import HTTPException

from ch07.db_connect import Session
from ch07.schema.student import StudentResponse, StudentCreate
from ch07.data import department as dept_data
from ch07.data import student as student_data


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

def get_by_dept_id(db: Session, dept_id: int) -> List[StudentResponse]:
    # 1. 해당하는 학과가 존재하는가? 없으면 예외처리
    dept = dept_data.find_by_id(db, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    students = student_data.find_by_department_id(db, dept_id)
    return [StudentResponse.model_validate(s) for s in students]

def update_student(db: Session, student_id: int, preferred_data: dict):
    student = student_data.find_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    dept = dept_data.find_by_id(db, preferred_data["preferred_department_id"])
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    student_data.update(db, student, preferred_data["preferred_department_id"])
    return StudentResponse.model_validate(student)

def assign_dept(db: Session):
    """
    1. 공통과정을 제외한 전체 학과 조회
    2. 학과별 희망학생을 score 내림차순으로 정렬
    3. 상위 personnel 명은 해당 학과로 확정
    4. 초과 학생은 잔여 정원이 있는 학과로 자동배정
    """
    depts = dept_data.find_all_except_default(db)

    # 학과별 배정 인원 추적
    assigned_count = {dept.id: 0 for dept in depts}
    overflow_students = []

    # 희망 학과가 없는 경우는 없다고 가정
    for dept in depts:
        # 해당 학과에 지원한 학생들 조회(내림차순) 100->99->90
        students = student_data.find_by_preferred_dept(db, dept.id)

        for i, student in enumerate(students):
            if i < dept.personnel:
                student.department_id = dept.id
                assigned_count[dept.id] += 1
            else:
                overflow_students.append(student)

    # 초과 학생 처리 -> 남은 순서대로 배정
    for student in overflow_students:
        for dept in depts:
            remain = dept.personnel - assigned_count[dept.id]
            if remain > 0:
                student.department_id = dept.id
                assigned_count[dept.id] += 1
                break
    db.commit()
    return {"message": "학과 배정이 완료되었습니다."}


