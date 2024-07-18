from fastapi import APIRouter, Depends, HTTPException
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



@router.get('/get/all')
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(notes_model.Notes).all()
    if not notes:
        raise HTTPException(status_code=400, detail='no notes exists')
    return {'data': notes}

@router.get('/get/{id}')
def get_notes_by_id(id: int, db: Session = Depends(get_db)):
    notes = db.query(notes_model.Notes).filter(notes_model.Notes.id == id).first()
    if not notes:
        raise HTTPException(status_code=400, detail='No note with the given id')
    return {
        'data': notes
    }

@router.delete('/delete/{id}')
def delete_notes(id: int, db: Session = Depends(get_db)):
    db.query(notes_model.Notes).filter(notes_model.Notes.id == id).delete(synchronize_session=False)
    db.commit()
    return {
        'message': 'note deleted'
    }


@router.put('/update/{id}')
def update_notes(id: int, request: notes_schema.Notes, db: Session = Depends(get_db)):
    notes = db.query(notes_model.Notes).filter(notes_model.Notes.id == id)
    if not notes.first():
        raise HTTPException(status_code=400, detail='No note found')
    notes.update(request.model_dump())
    db.commit()
    return {
        'message': 'note updated' 
    }