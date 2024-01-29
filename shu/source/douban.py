from parsel import Selector
import json

def url_for(isbn):
    return f'https://book.douban.com/isbn/{isbn}/'

def parse(html):
    selector = Selector(html)

    fields = parse_info_block(selector)

    book = dict(
        title=parse_title(selector),
        identifiers={'douban': parse_douban_id(selector)},
        cover_url=parse_cover_url(selector),
        rating=parse_rating(selector),
    )

    if '副标题' in fields:
        book['subtitle'] = fields['副标题']
    if '原作名' in fields:
        book['original_title'] = fields['原作名']

    if 'ISBN' in fields:
        book['identifiers']['isbn'] = fields['ISBN']
    if '统一书号' in fields:
        book['identifiers']['csbn'] = fields['统一书号']

    if '作者' in fields:
        book['authors'] = fields['作者']
    if '译者' in fields:
        book['translators'] = fields['译者']

    if '出版社' in fields:
        book['press'] = fields['出版社']
    if '出品方' in fields:
        book['producers'] = fields['出品方']
    if '出版年' in fields:
        book['pubdate'] = fields['出版年']
    if '丛书' in fields:
        book['series'] = fields['丛书']
        book['series_id'] = selector.css('#info').re(r'https://book.douban.com/series/([0-9]*)')[0]


    if '页数' in fields:
        book['pages'] = fields['页数']
    if '定价' in fields:
        book['price'] = fields['定价']

    if '装帧' in fields:
        book['binding'] = fields['装帧']
    
    return book

def parse_title(selector):
    return parse_meta_block(selector, 'og:title')

def parse_douban_url(selector):
    return parse_meta_block(selector, 'og:url')

def parse_douban_id(selector):
    return parse_douban_url(selector).strip('/').split('/')[-1]

def parse_cover_url(selector):
    return parse_meta_block(selector, 'og:image')

def parse_description(selector):
    return parse_meta_block(selector, 'og:description')

def parse_rating(selector):
    return selector.css('strong.rating_num::text').get().strip()

def parse_meta_block(selector, property):
    return selector.xpath(f'//meta[@property="{property}"]/@content').get()

def parse_json_block(selector):
    ''' Parse json block in html '''
    json_block = selector.xpath('//script[@type="application/ld+json"]/text()')
    return json.loads(json_block.get())

def parse_info_block(selector):
    ''' Parse lines for info block'''
    info = selector.xpath('string(//div[@id="info"])').get().strip()
    lines = [line.strip() for line in info.splitlines() if line.strip() != ""]

    fields = {}
    key = None
    value = None
    for line in lines:
        if ":" in line:
            key, value = [x.strip() for x in line.split(":", 1)]
            fields[key] = [] if value == "" else [value]
        elif line != "/":
            fields[key].append(line)

    for k, v in fields.items():
        if len(v) == 1:
            fields[k] = v[0]

    return fields

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        html = f.read()
        print(parse(html))
