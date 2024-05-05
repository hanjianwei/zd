import click
from click.decorators import pass_context
from devtools import pprint
from loguru import logger
import os


from .douban import Douban
from .client import Client
from .repo import Repo

# Setup proxy pool using:
# export PROXY_POOL="http://127.0.0.1:5010/get/"
client = Client(proxy_pool=os.getenv("PROXY_POOL"))

@click.group()
@click.option("--repo-dir", "-d", default=".")
@pass_context
def main(ctx, repo_dir):
    ctx.ensure_object(dict)
    ctx.obj['repo_dir'] = repo_dir

@main.command()
@pass_context
def init(ctx):
    Repo(ctx.obj['repo_dir'], create_dirs=True)

def process_item(kind, douban_id, handler=pprint):
    html = yield Douban.make_url(kind, douban_id)
    if html is None:
        logger.error(f"{kind} Not found")
        return
    douban = Douban(html, kind=kind)
    data = douban.subject

    while douban.next_url:
        html = yield douban.next_url
        douban = Douban(html, kind=kind)
        data.items.extend(douban.subject.items)

    handler(data)

@main.command()
@click.argument("douban_id_or_isbn")
def book(douban_id_or_isbn):
    client.get(process_item('book', douban_id_or_isbn))

@main.command()
@click.argument("douban_id")
def movie(douban_id):
    client.get(process_item('movie', douban_id))

@main.command()
@click.argument("douban_id")
def music(douban_id):
    client.get(process_item('music', douban_id))

@main.command()
@click.argument("doulist_id")
def doulist(doulist_id):
    client.get(process_item('doulist', doulist_id))

@main.command()
@click.argument("series_id")
def series(series_id):
    client.get(process_item('series', series_id))

if __name__ == "__main__":
    main()
