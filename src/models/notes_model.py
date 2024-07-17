from sqlalchemy import Column, Integer, String

from databases.database import Base

class Notes(Base):
    __tablename__ = 'notes'
    __allow_unmapped__ = True
    id= Column(Integer, primary_key=True, index=True)
    title= Column(String)
    description= Column(String)
