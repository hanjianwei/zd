from pathlib import Path
from loguru import logger
import uuid

class Repo:
    def __init__(self, repo_dir='.', create_dirs=False):
        self.repo_dir = Path(repo_dir)

        self.books_dir = self.repo_dir / 'books'
        self.movies_dir = self.repo_dir / 'movies'
        self.music_dir = self.repo_dir / 'music'

        if create_dirs:
            for f in [self.books_dir, self.movies_dir, self.music_dir]:
                f.mkdir(parents=True, exist_ok=True)

    def book_dir(self, book):
        for i in ['isbn', 'csbn', 'douban']:
            if i in book.identifiers:
                return self.books_dir / i / book.identifiers[i]

        logger.warning("No identifiers found")
        return self.books_dir / 'unknown' / str(uuid.uuid1())

    def add_book(self, book):
        book_dir = self.book_dir(book)
        if book_dir.exists():
            self.update_book(book)

    def update_book(self, book):
        pass


        
