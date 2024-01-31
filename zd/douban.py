from typing import Optional
from parsel import Selector
import json

from functools import cached_property

from .utils import is_isbn

class Douban:
    def __init__(self, html:str, kind=None):
        self.html = html
        self.selector = Selector(html)
        self.kind = kind or self.detect_kind()
        self.next_url = None # For paged results

        self.subject = self.parse()

    @classmethod
    def make_url(cls, kind, id_):
        if kind == 'book' and is_isbn(id_): 
            return f"https://book.douban.com/isbn/{id_}/"
        if kind in ['book', 'movie', 'music']:
            return f'https://{kind}.douban.com/subject/{id_}/'
        elif kind == 'series':
            return f'https://book.douban.com/series/{id_}/'

        raise Exception(f'Unknown kind: {kind} or args: {id_}')

    def parse(self):
        if self.kind == 'book':
            return self.parse_book()
        elif self.kind == 'video.movie':
            return self.parse_movie()
        elif self.kind == 'music.album':
            return self.parse_music()
        elif self.kind == 'series':
            return self.parse_series()
        else:
            raise Exception(f'Unknown media type: {self.kind}')

    def parse_book(self):
        book = dict(
            title=self.title,
            authors=self.authors,
            identifiers={ 'douban': self.douban_id },
            url=self.url,
            cover_url=self.cover_url,
            rating=self.rating,
        )

        if '丛书' in self.info:
            book['series'] = self.info['丛书']
            book['series_id'] = self.selector.css('#info').re(r'https://book.douban.com/series/([0-9]*)')[0]

        if 'ISBN' in self.info:
            book['identifiers']['isbn'] = self.info['ISBN']
        if '统一书号' in self.info:
            book['identifiers']['csbn'] = self.info['统一书号']

        # Copy other info from info block
        attrs_map = {
            'subtitle': '副标题',
            'original_title': '原作名',
            'translators': '译者',
            'press': '出版社',
            'producers': '出品方',
            'pubdate': '出版年',
            'pages': '页数',
            'price': '定价',
            'binding': '装帧',
        }

        for k, v in attrs_map.items():
            if v in self.info:
                book[k] = self.info[v]
        
        return book

    def parse_series(self):
        text = self.selector.xpath('string(//div[@id="content"]//div[@class="pl2"])').get().strip()
        props = self.parse_properties(text)

        series = dict(
            title=self.title,
            identifiers={ 'douban': self.douban_id },
            url=self.url,
            press=props['出版社'],
            count=props['册数'],
        )

        book_elems = self.selector.css("li[class='subject-item'] div.info")
        series['books'] = [self.parse_series_book(elem) for elem in book_elems]
        self.next_url = self.selector.css("span.next a::attr(href)").get()

        return series

    def parse_series_book(self, elem):
        book = {}
        book['title'] = elem.css('a::text').get().strip()
        book['url'] = elem.css('a::attr(href)').get().strip()
        book['identifiers'] = { 'douban': book['url'].strip('/').split('/')[-1] }
        book['intro'] = elem.css('div.pub::text').get().strip()

        return book

    def parse_movie(self):
        movie = dict(
            title=self.title,
            directors=self.directors,
            casts=self.actors,
            identifiers={ 'douban': self.douban_id },
            url=self.url,
            cover_url=self.cover_url,
            rating=self.rating,
        )

        if 'IMDb' in self.info:
            movie['identifiers']['imdb'] = self.info['IMDb']

        if '上映日期' in self.info:
            movie['pubdates'] = self.info['上映日期']
        elif '首播' in self.info:
            movie['pubdates'] = self.info['首播']

        # Copy other info from info block
        attrs_map = {
            'alt_title': '又名',
            'writers': '编剧',
            'genres': '类型',
            'durations': '片长',
            'countries': '制片国家/地区',
            'languages': '语言',
            'website': '官方网站',
            'current_season': '季数',
            'episodes_count': '集数',
        }

        for k, v in attrs_map.items():
            if v in self.info:
                movie[k] = self.info[v]

        for k in ['alt_title', 'pubdates', 'writers', 'genres', 'durations', 'countries', 'languages']:
            if k in movie:
                movie[k] = [x.strip() for x in movie[k].split('/')]

        return movie

    def parse_music(self):
        music = dict(
            title=self.title,
            authors=self.musicians,
            identifiers={ 'douban': self.douban_id },
            url=self.url,
            cover_url=self.cover_url,
            rating=self.rating,
        )

        if '条形码' in self.info:
            music['identifiers']['barcode'] = self.info['条形码']

        # Copy other info from info block
        attrs_map = {
            'alt_title': '又名',
            'pubdate': '发行时间',
            'genres': '流派',
            'media': '介质',
            'discs': '唱片数',
            'kind': '专辑类型',
            'press': '出版者',
        }

        for k, v in attrs_map.items():
            if v in self.info:
                music[k] = self.info[v]

        return music

    def detect_kind(self):
        return self.parse_meta('og:type')

    @cached_property
    def title(self):
        return self.parse_meta('og:title') or self.selector.css('title::text').get().strip()

    @cached_property
    def authors(self):
        return self.parse_meta('book:author', True)

    @cached_property
    def directors(self):
        return self.parse_meta('video:director', True)

    @cached_property
    def actors(self):
        return self.parse_meta('video:actor', True)

    @cached_property
    def musicians(self):
        return self.parse_meta('music:musician', True)

    @cached_property
    def durations(self):
        return self.parse_meta('video:duration', True)

    @cached_property
    def url(self):
        if self.kind == 'series':
            return self.selector.css("span[class='pl rr'] a").attrib['href'].split('?')[0]
        else:
            return self.parse_meta('og:url')

    @cached_property
    def douban_id(self):
        return self.url.strip('/').split('/')[-1]

    @cached_property
    def cover_url(self):
        return self.parse_meta('og:image')

    @cached_property
    def description(self):
        return self.parse_meta('og:description')

    @cached_property
    def rating(self):
        node = self.selector.css('strong.rating_num::text').get()
        return "0" if node is None else node.strip()

    @cached_property
    def info(self):
        ''' Parse lines for info block'''
        text = self.selector.xpath('string(//div[@id="info"])').get().strip()
        return self.parse_properties(text)

    def parse_properties(self, text):
        ''' Parse lines for info block'''
        lines = [line.strip() for line in text.splitlines() if line.strip() != ""]

        props = {}
        key = None
        value = None
        for line in lines:
            if ":" in line:
                key, value = [x.strip() for x in line.split(":", 1)]
                props[key] = [] if value == "" else [value]
            elif line != "/":
                props[key].append(line)

        for k, v in props.items():
            if len(v) == 1:
                props[k] = v[0]

        return props

    @cached_property
    def json(self):
        ''' Parse json block in html '''
        text = self.selector.xpath('//script[@type="application/ld+json"]/text()')
        return json.loads(text.get())

    def parse_meta(self, property, multiple=False):
        node = self.selector.xpath(f'//meta[@property="{property}"]/@content')
        return node.getall() if multiple else node.get()


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        html = f.read()
        if len(sys.argv) > 2:
            print(Douban(html, kind=sys.argv[2]).subject)
        else:
            print(Douban(html).subject)
