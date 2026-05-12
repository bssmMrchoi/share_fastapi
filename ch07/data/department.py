from ch07.db_connect import Session
from ch07.model.department import Department


def insert(db:Session, name:str, personnel:int):
    dept = Department(name = name, personnel = personnel)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

def find_by_name(db:Session, name:str):
    return db.query(Department).filter(Department.name == name).first()

def find_by_id(db:Session, id:int) -> Department:
    return db.query(Department).filter(Department.id == id).first()

def find_all(db:Session):
    return db.query(Department).all()


def delete(db: Session, id: int):
    db.query(Department).filter(Department.id == id).delete()
    db.commit()