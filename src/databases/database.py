from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker, declarative_base


NOTES_DATABASE_URL = 'sqlite:///./src/databases/notes.db'


engine = create_engine(url=NOTES_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        