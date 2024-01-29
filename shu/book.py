from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str
    identifiers: dict[str, str] = Field(default_factory=dict)
    authors: list[str] = Field(default_factory=list)
    subtitle: str = ""
    origin_title: str = ""
    alt_title: str = ""
    translators: list[str] = Field(default_factory=list)
    press: str = ""
    producers: list[str] = Field(default_factory=list)
    pubdate: str = ""
    series_id: str = ""
    series: str = ""
    pages: int = 0
    price: str = ""
    binding: str = ""
    intro: str = ""
    toc: str = ""
    languages: list[str] = Field(default_factory=list)
    cover_url: str = ""
    tags: list[str] = Field(default_factory=list)
    rating: str = ""
    comments: str = ""
