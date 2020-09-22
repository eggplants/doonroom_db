import datetime
import re
from typing import cast, List, Callable, Match, Sequence, Optional, TypedDict
from bs4.element import Tag
from bs4 import BeautifulSoup as BS


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
    buy_links: List[str]
    tags: List[str]
    type: str


class Parser(object):

    def __init__(self, category: str) -> None:
        """Init."""
        if category not in ['hypno', 'dojin']:
            raise ParseUnknownCategory("Unknown Category: %s" % category)
        else:
            self.category = category

    def parse(self, path: str) -> List[DatasDict]:
        """Extract required information from the page sources and scrape it."""

        def convert_product_from_aff(link: str) -> str:
            """Convert an affiliated link into a raw link."""
            aff_link = 'dlaf/={}link/work/aid/momonoyu/'
            product_path = 'work/=/product_'
            return link.replace(
                aff_link.format('/t/i/'), product_path
            ).replace(
                aff_link.format('/'), product_path
            ).replace('doonroom-001/', '')

        def groups(result: Match[str]) -> Sequence[str]:
            return result.groups()

        # Get rating points from a rating bar.
        rate: Callable[[Optional[Match[str]]], int] = lambda bar:\
            int(groups(bar)[0]) if not not bar else 99

        # Extract texts from each node in an array.
        ext_text_node: Callable[[Tag], Optional[str]] = lambda v: \
            (v.text if hasattr(v, 'text') else None)
        ext_text: Callable[[List[Tag]], List[str]] = lambda arr:\
            [i for i in map(ext_text_node, arr) if i]

        # Extract href from a node.
        ext_href: Callable[[Tag], Optional[str]] = lambda v:\
            (v['href'] if 'href' in v.attrs else None)

        print(path, end="\r")
        bs = BS(open(path, 'r'), 'lxml')
        pages = bs.find_all(
            'article', attrs={"itemtype": "http://schema.org/BlogPosting"})

        ext_page_data = []
        for page in pages:
            data = cast('DatasDict', {})

            data['page_id'] = int(re.findall(
                r'\d+', page.h1.a['href']
            )[0])

            data['article_link'] = page.h1.a['href']

            data['post_date'] = int(
                datetime.datetime.fromisoformat(
                    page.time['datetime']
                ).timestamp())

            data['title'] = page.h1.a.text

            data['body'] = page.select_one('div.article-body-inner').get_text()

            data['rating'] = rate(re.search(
                r'[■□]{10}　(\d+)', page.get_text()))

            data['category'] = page.find_all(
                'dd', class_='article-category1'
            )[-1].text

            hrefs = list(map(
                ext_href, page.find_all('a', href=True)))
            data['buy_links'] = list(set(
                [convert_product_from_aff(i)
                 for i in hrefs
                 if i is not None and 'doonroom.blog.jp' not in i]))

            data['tags'] = ext_text(page.dl.find_all('a'))

            data['type'] = self.category

            ext_page_data.append(data)

        print(' ' * 30, end='\r')
        return ext_page_data
