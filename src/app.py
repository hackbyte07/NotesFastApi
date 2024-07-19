from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from databases.database import  engine, Base
from routers import notes_router, users_router

app = FastAPI(title='Notes api', version='0.1.0')
load_dotenv('.env')

Base.metadata.create_all(bind=engine)

 
@app.get('/')
def index():
    return {'Welcome to notes'}


app.include_router(users_router.router)
app.include_router(notes_router.router)

uvicorn.run(app=app, port=1111) 