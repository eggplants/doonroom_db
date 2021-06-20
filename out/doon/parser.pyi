from bs4.element import Tag as Tag
from typing import Any, List, TypedDict

class ParseUnknownCategory(Exception): ...

class DatasDict(TypedDict):
    page_id: int
    article_link: str
    post_date: int
    title: str
    body: str
    rating: int
    category: str
    buy_links: List[str]
    tags: List[str]
    type: str
    plays: List[str]

class Parser:
    category: Any = ...
    def __init__(self, category: str) -> None: ...
    def parse(self, path: str) -> List[DatasDict]: ...
