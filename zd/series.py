from pydantic import BaseModel, Field
from .book import Book

class Series(BaseModel):
    title: str
    identifiers: dict[str, str] = Field(default_factory=dict)
    url: str = ""
    press: str = ""
    count: int = 0
    books: list[Book] = Field(default_factory=list)
    intro: str = ""
    tags: list[str] = Field(default_factory=list)
