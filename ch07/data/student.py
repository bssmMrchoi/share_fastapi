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