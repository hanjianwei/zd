import click
import yaml


from . import douban
from .book import Book
from .client import http_get


@click.group()
def main():
    pass

@main.command()
@click.argument("isbn")
def get(isbn):
    html = http_get(douban.book_url(isbn))

    if html is None:
        print("Book Not found")
        return

    info = douban.parse_book(html)
    book = Book(**info)
    print(yaml.dump(book.__dict__, allow_unicode=True, sort_keys=False))


if __name__ == "__main__":
    main()

    # c = Calibre()
    # calibre_id = c.search_isbn(isbn)
    # print(calibre_id)

    # cmd = "calibredb add -e -t {title} -T HomeLibrary".format(title=title)

    # if "作者" in meta:
    #     cmd += " -a {作者}".format(**meta)
    # if "ISBN" in meta:
    #     cmd += " -i {ISBN}".format(**meta)
    #     # if '丛书' in meta:

    # # Download cover image
    # if img is not None:
    #     cover = meta["ISBN"] + img[-4:]
    #     with open(cover, "wb") as f:
    #         f.write(requests.get(img).content)
    #         cmd += " -c {cover}".format(cover=cover)

    # print(cmd)
