from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2
from jose import JWTError, jwt
from fastapi.security  import OAuth2PasswordBearer

from schemas.users_schema import TokenData

SECRET_KEY = str(os.getenv('jwt_secret_key'))
ALGORITHM  = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTE = 120


oAuth2Scheme = OAuth2PasswordBearer(tokenUrl='auth_utils')

def genrate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTE)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def get_current_user(token: str = Depends(oAuth2Scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        email: str | None = payload.get('sub') 
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authorized', headers={'WWW-Authenticate':'Bearer'})
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authorized', headers={'WWW-Authenticate':'Bearer'})
     