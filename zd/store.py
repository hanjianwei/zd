from pydantic import BaseModel, Field
from pathlib import Path
from loguru import logger
from pathvalidate import sanitize_filename
import uuid
import frontmatter
from functools import cached_property

class Store(BaseModel):
    place: list[str] = Field(default_factory=list)
    amount: int = 1
    
