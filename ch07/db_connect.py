from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB 연결을 관리한느 객체
engine = create_engine("sqlite:///school.db",
                       connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


