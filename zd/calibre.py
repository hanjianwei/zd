import subprocess

"""
❯ calibredb set_metadata -l
Title                                    Field name

ISBN                                     #isbn
Author sort                              author_sort
Authors                                  authors
Comments                                 comments
Cover                                    cover
Identifiers                              identifiers
Languages                                languages
Published                                pubdate
Publisher                                publisher
Rating                                   rating
Series                                   series
Series Index                             series_index
Size                                     size
Title sort                               sort
Tags                                     tags
Date                                     timestamp
Title                                    title
Cover                                    cover
"""


class Calibre:
    def __init__(self):
        pass

    def add_book(self, book):
        pass

    def update(self, bookid, book):
        pass

    def search_isbn(self, isbn):
        p = subprocess.run(
            'calibredb search "isbn:{}"'.format(isbn), shell=True, capture_output=True
        )
        return p.stdout.decode("utf-8").strip() if p.returncode == 0 else None
