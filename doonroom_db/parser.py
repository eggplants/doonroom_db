from __future__ import annotations

import datetime
import re
from typing import Match, Sequence, TypedDict, cast

from bs4 import BeautifulSoup
from bs4.element import Tag


class ParseUnknownCategory(Exception):
    pass


class DatasDict(TypedDict):
    page_id: int
    article_link: str
    post_date: int
    title: str
    body: str
    rating: int
    category: str
    buy_links: list[str]
    tags: list[str]
    type: str
    plays: list[str]


class Parser(object):
    def __init__(self, category: str) -> None:
        """Init."""
        if category not in ["hypno", "dojin"]:
            raise ParseUnknownCategory("Unknown Category: %s" % category)
        else:
            self.category = category

    def parse(self, path: str) -> list[DatasDict]:
        """Extract required information from the page sources and scrape it."""

        print(path, end="\r")
        bs = BeautifulSoup(open(path, "r").read(), "lxml")
        pages = bs.find_all(
            "article", attrs={"itemtype": "http://schema.org/BlogPosting"}
        )

        ext_page_data = []
        for page in pages:
            page = cast(Tag, page)
            data = cast(DatasDict, {})

            data["page_id"] = int(re.findall(r"\d+", page.h1.a["href"])[0])

            data["article_link"] = page.h1.a["href"]

            data["post_date"] = int(
                datetime.datetime.fromisoformat(page.time["datetime"]).timestamp()
            )

            data["title"] = page.h1.a.text

            data["body"] = page.select_one("div.article-body-inner").get_text()

            data["rating"] = self.__get_rate(
                re.search(r"[■□]{10}　(\d+)", page.get_text())
            )

            data["category"] = page.find_all("dd", class_="article-category1")[-1].text

            hrefs = list(map(self.__extract_href, page.find_all("a", href=True)))
            data["buy_links"] = list(
                {
                    self.__convert_product_from_aff(i)
                    for i in hrefs
                    if i is not None and "doonroom.blog.jp" not in i
                }
            )

            data["tags"] = self.__extract_text(page.dl.find_all("a"))

            plays = page.select_one(
                'span[style="color: rgb(238, 102, 0);"],' 'span[style="color:#ee6600"]'
            )

            if plays:
                data["plays"] = re.findall(r"\w+", plays.text)
            else:
                data["plays"] = []

            data["type"] = self.category

            ext_page_data.append(data)

        print(" " * 30, end="\r")
        return ext_page_data

    @staticmethod
    def __convert_product_from_aff(link: str) -> str:
        """Convert an affiliated link into a raw link."""
        aff_link = "dlaf/={}link/work/aid/momonoyu/"
        product_path = "work/=/product_"
        return (
            link.replace(aff_link.format("/t/i/"), product_path)
            .replace(aff_link.format("/"), product_path)
            .replace("doonroom-001/", "")
        )

    @staticmethod
    def __get_rate(bar: Match[str] | None) -> int:
        """Get rating points from a rating bar."""

        def groups(result: Match[str]) -> Sequence[str]:
            return result.groups()

        return int(groups(bar)[0]) if bar is not None else 99

    @staticmethod
    def __extract_text(arr: list[Tag]) -> list[str]:
        """Extract texts from each node in an array."""

        def ext_text_node(v: Tag) -> str | None:
            return v.text if hasattr(v, "text") else None

        return [i for i in map(ext_text_node, arr) if i is not None]

    @staticmethod
    def __extract_href(v: Tag) -> str | None:
        """Extract href from a node."""
        return str(v["href"]) if "href" in v.attrs else None
