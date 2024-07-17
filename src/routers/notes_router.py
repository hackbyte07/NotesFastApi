from fastapi import APIRouter, Depends
from databases.database import get_db
from schemas import notes_schema
from models import notes_model
from sqlalchemy.orm import Session

router = APIRouter(tags=["Notes"], prefix='/notes')


@router.get('/')
def index():
    return {'welcome to notes'}


@router.post('/add')
def add_note(request: notes_schema.Notes, db: Session = Depends(get_db) ):
    new_note = notes_model.Notes(id =  request.id, title= request.title, description= request.description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {'message': 'note added'}

