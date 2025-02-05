from typing import Optional
from pydantic import BaseModel


class Signup(BaseModel):
    id: int
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
     
class TokenData(BaseModel):
    email: Optional[str] = None
       
    