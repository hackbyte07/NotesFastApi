from pydantic import BaseModel


class Notes(BaseModel):
    id: int
    title: str
    description: str