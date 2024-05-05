from pydantic import BaseModel, Field
from pathlib import Path
from loguru import logger
from pathvalidate import sanitize_filename
import uuid
import frontmatter
from functools import cached_property

class Book(BaseModel):
    title: str
    subtitle: str = ""
    origin_title: str = ""
    alt_title: str = ""
    url: str = ""
    cover_url: str = ""
    identifiers: dict[str, str] = Field(default_factory=dict)
    authors: list[str] = Field(default_factory=list)
    translators: list[str] = Field(default_factory=list)
    press: str = ""
    producers: list[str] = Field(default_factory=list)
    pubdate: str = ""
    series_id: str = ""
    series: str = ""
    volumes: int = 1
    pages: int = 0
    price: str = ""
    binding: str = ""
    intro: str = ""
    toc: str = ""
    languages: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    rating: str = ""
    comments: str = ""

    def main_id(self):
        if not self.identifiers:
            logger.warning("No identifiers found")
            return 'unknown', str(uuid.uuid1())

        for i in ['isbn', 'csbn', 'douban']:
            if i in self.identifiers:
                return i, self.identifiers[i]
        else:
            return list(self.identifiers.items())[0]

    @cached_property
    def folder(self):
        id_type, id_value = self.main_id()
        return Path('books') / id_type / id_value

    @cached_property
    def index(self):
        return self.folder / f'{sanitize_filename(self.title)}.md'


    def save(self, repo_dir, exist_ok=True):
        folder = repo_dir / self.folder
        index = repo_dir / self.index

        if index.exists() and not exist_ok:
            logger.error(f"{index} already exists")
            return

        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)

        post = frontmatter.load(index) if index.exists() else frontmatter.Post('')
        post.metadata |= self.model_dump(exclude_unset=True)

        with open(index, 'w') as f:
            f.write(frontmatter.dumps(post))







