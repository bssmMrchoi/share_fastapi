from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ch07.db_connect import Base


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    personnel = Column(Integer, nullable=False)

    # 1. 이 학과 학생 목록을 바로 조회 할 수 있음 -> 매번 select 안해도됌
    students = relationship(
        "Student",
        back_populates="department",
        foreign_keys="Student.department_id",
    )

    preferred_students = relationship(
        "Student",
        back_populates="preferred_department",
        foreign_keys="Student.preferred_department_id",
    )