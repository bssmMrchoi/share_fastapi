from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# DB 연결을 관리한느 객체
engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

# Base를 상속받은 클래스는 자동으로 테이블과 매핑
Base = declarative_base()
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    personnel = Column(Integer)

# 실제 DB 작업을 처리
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == '__main__':
    # 앱 시작시 Base에 등록된 모든 모델을 테이블로 생성
    Base.metadata.create_all(engine)
    with get_db() as db:
        dept = Department(name="임베디드SW과", personnel=32)
        db.add(dept)
        db.commit()