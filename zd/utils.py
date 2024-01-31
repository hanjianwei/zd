def is_isbn(isbn):
    return len(isbn) in [10, 13] and isbn.isdigit()

def is_imdb(imdb):
    return imdb.startswith('tt') and imdb[2:].isdigit()
