from pydantic import BaseModel, Field
from .movie import Movie
from .book import Book

class FavList(BaseModel):
    title: str
    url: str = ""
    identifiers: dict[str, str] = Field(default_factory=dict)
    count: int = 0
    items: list[Book | Movie] = Field(default_factory=list)
    intro: str = ""
    tags: list[str] = Field(default_factory=list)
    comments: str = ""
