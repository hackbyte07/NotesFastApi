import os
from fastapi import APIRouter, Depends, HTTPException, status

from databases.database import get_db
from models import user_model
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas import users_schema
from utils.auth_utils import genrate_token


router = APIRouter(tags=['users'], prefix='/users')

pwd_context = CryptContext(schemes=['bcrypt'])

jwt_secret_key = os.getenv('jwt_secret_key')

@router.get('/')
def index():
    return {'login to use 😆'}

@router.post('/login')
def login(request: users_schema.Login, db: Session = Depends(get_db)):
    user = db.query(user_model.Users).filter(user_model.Users.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not pwd_context.verify(str(request.password), str(user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    token = genrate_token({'sub': user.email})
    return {
        'token': token,
        'token type': 'Bearer'
    }
    
    
@router.post('/signup')
def signup(request: users_schema.Signup, db: Session = Depends(get_db)):
    user_exists = db.query(user_model.Users).filter(user_model.Users.email == request.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Users already exists')
    hashed_password: str = pwd_context.encrypt(request.password)
    new_user = user_model.Users(id=request.id, name = request.name, email = request.email, password = hashed_password)

    db.add(new_user)
    db.commit()
    return {
        'message': 'user created successfully'
    }

