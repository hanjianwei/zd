from pydantic import BaseModel, Field

class Music(BaseModel):
    title: str
    alt_title: str = ""
    url: str = ""
    cover_url: str = ""
    identifiers: dict[str, str] = Field(default_factory=dict)
    authors: list[str] = Field(default_factory=list)
    genres: list[str] = Field(default_factory=list)
    press: str = ""
    pubdate: str = ""
    media: str = ""
    discs: int = 0
    kind: str = ""
    intro: str = ""
    tags: list[str] = Field(default_factory=list)
    rating: str = ""
    comments: str = ""
