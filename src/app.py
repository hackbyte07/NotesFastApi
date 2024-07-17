from fastapi import FastAPI
import uvicorn
from databases.database import  engine, Base
from routers import notes_router


app = FastAPI(title='Notes app')

Base.metadata.create_all(bind=engine)


@app.get('/')
def index():
    return {'Welcome to notes'}

app.include_router(notes_router.router)

uvicorn.run(app=app) 