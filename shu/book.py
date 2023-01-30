from dataclasses import dataclass, field


@dataclass
class Book:
    title: str
    identifiers: dict[str, str]
    authors: list[str]
    subtitle: str = ""
    origin_title: str = ""
    alt_title: str = ""
    translators: list[str] = field(default_factory=list)
    press: str = ""
    producers: list[str] = field(default_factory=list)
    pubdate: str = ""
    series_id: str = ""
    series: str = ""
    pages: int = 0
    price: str = ""
    binding: str = ""
    intro: str = ""
    toc: str = ""
    languages: list[str] = field(default_factory=list)
    cover_url: str = ""
    tags: list[str] = field(default_factory=list)
    rating: str = ""
    comments: str = ""
