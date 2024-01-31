import click
import yaml


from .douban import Douban
from .book import Book
from .movie import Movie
from .music import Music
from .series import Series
from .client import http_get


@click.group()
def main():
    pass

@main.command()
@click.argument("series_id")
def series(series_id):
    url = Douban.make_url('series', series_id)
    html = http_get(url)
    if html is None:
        print("Series Not found")
        return
    douban = Douban(html, kind='series')
    info = douban.subject

    while douban.next_url:
        html = http_get(douban.next_url)
        douban = Douban(html, kind='series')
        info['books'].extend(douban.subject['books'])

    series = Series(**info)
    print(yaml.dump(series.model_dump(exclude_unset=True), allow_unicode=True, sort_keys=False))

@main.command()
@click.argument("douban_id_or_isbn")
def book(douban_id_or_isbn):
    url = Douban.make_url('book', douban_id_or_isbn)
    html = http_get(url)

    if html is None:
        print("Book Not found")
        return

    info = Douban(html).subject
    book = Book(**info)
    print(yaml.dump(book.__dict__, allow_unicode=True, sort_keys=False))

@main.command()
@click.argument("douban_id")
def movie(douban_id):
    url = Douban.make_url('movie', douban_id)
    html = http_get(url)
    if html is None:
        print("Movie Not found")
        return
    info = Douban(html).subject
    movie = Movie(**info)
    print(yaml.dump(movie.model_dump(exclude_unset=True), allow_unicode=True, sort_keys=False))

@main.command()
@click.argument("douban_id")
def music(douban_id):
    url = Douban.make_url('music', douban_id)
    html = http_get(url)
    if html is None:
        print("Music Not found")
        return
    info = Douban(html).subject
    music = Music(**info)
    print(yaml.dump(music.model_dump(exclude_unset=True), allow_unicode=True, sort_keys=False))

if __name__ == "__main__":
    main()
