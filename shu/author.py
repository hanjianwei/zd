from dataclasses import dataclass


@dataclass
class Author:
    name: str
    cn_name: str
    citizenship: str
    born: str
    died: str
    intro: str
