from dataclasses import dataclass


@dataclass
class Author:
    name: str
    alt_names: dict[str, str]
    citizenship: str
    born: str
    died: str
    intro: str

    def __str__(self):
        return f"[{self.citizenship}]{self.name}"
