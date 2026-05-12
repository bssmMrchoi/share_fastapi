from ch07.db_connect import Session
from ch07.model.student import Gender, Student


def create(db:Session, name:str, gender:Gender, score:float,
           department_id:int, preferred_department_id:int):
    student = Student(
        name=name,
        gender=gender,
        score=score,
        department_id=department_id,
        preferred_department_id=preferred_department_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def find_by_department_id(db:Session, dept_id:int):
    return db.query(Student).filter(Student.department_id == dept_id).all()

def find_by_id(db:Session, student_id:int):
    return db.query(Student).filter(Student.id == student_id).first()

def update(db:Session, student: Student, preferred_department_id:int):
    setattr(student, "preferred_department_id", preferred_department_id)
    db.commit()
    db.refresh(student)
    return student

def find_by_preferred_dept(db:Session, preferred_department_id:int):
    # 희망 학과 기준으로 학생 목록 조회(score 내림차순)
    return (db.query(Student)
            .filter(Student.preferred_department_id == preferred_department_id)
            .order_by(Student.score.desc())
            .all()
            )