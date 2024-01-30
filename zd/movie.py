from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str
    alt_title: list[str] = Field(default_factory=list)
    url: str = ""
    cover_url: str = ""
    identifiers: dict[str, str] = Field(default_factory=dict)
    directors: list[str] = Field(default_factory=list)
    writers: list[str] = Field(default_factory=list)
    casts: list[str] = Field(default_factory=list)
    genres: list[str] = Field(default_factory=list)
    pubdates: list[str] = Field(default_factory=list)
    year: str = ""
    durations: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    website: str = ""
    seasons_count: int = 0
    current_season: int = 0
    episodes_count: int = 0
    intro: str = ""
    languages: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    rating: str = ""
    comments: str = ""
