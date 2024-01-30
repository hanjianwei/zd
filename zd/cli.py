import click
import yaml


from .douban import Douban
from .book import Book
from .client import http_get


@click.group()
def main():
    pass

@main.command()
@click.argument("isbn")
def book(isbn):
    url = Douban.make_url('book', isbn=isbn)
    html = http_get(url)

    if html is None:
        print("Book Not found")
        return

    info = Douban(html).subject
    book = Book(**info)
    print(yaml.dump(book.__dict__, allow_unicode=True, sort_keys=False))

@main.command()
@click.argument("sid")
def movie(sid):
    url = Douban.make_url('movie', id=sid)
    html = http_get(url)
    if html is None:
        print("Movie Not found")
        return
    info = Douban(html).subject
    print(yaml.dump(info, allow_unicode=True, sort_keys=False))

@main.command()
@click.argument("sid")
def music(sid):
    url = Douban.make_url('music', id=sid)
    html = http_get(url)
    if html is None:
        print("Music Not found")
        return
    info = Douban(html).subject
    print(yaml.dump(info, allow_unicode=True, sort_keys=False))

if __name__ == "__main__":
    main()
