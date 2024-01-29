from pydantic import BaseModel

class Series(BaseModel):
    id: str
    title: str
