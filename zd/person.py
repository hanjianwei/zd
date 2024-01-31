from pydantic import BaseModel

'''
class Author:
    def __init__(info):
        matched = re.match(r"(\[.*\])?(.*)", info.strip())
        name = matched.group(2).strip()
        country = matched.group(1)
        if country is not None:
            country = self.country.strip("[] ")

    def __str__(:
        return f"[{country}]{self.name}"


def parse_authors(info):
    authors = [Author(a) for a in info.strip().split("/")]
    if authors[0].country is not None:
        for a in authors[1:]:
            if a.country is None:
                a.country = authors[0].country

    return authors
'''
class Person(BaseModel):
    name: str
    alt_names: dict[str, str]
    citizenship: str
    born: str
    died: str
    intro: str

