import datetime
import re
from typing import List
from bs4 import BeautifulSoup as BS


class ParseUnknownCategory(Exception):
    pass


class Parser(object):

    def __init__(self, category: str) -> None:
        """Init."""
        if category not in ['hypno', 'dojin']:
            raise ParseUnknownCategory("Unknown Category: %s" % category)

        self.category = category

    def parse(self, path: str) -> List[dict]:
        """Extract required information from the page sources and scrape it."""

        def ext_text_from_array(arr: List) -> List[str]:
            """Extract texts from each node in an array."""
            return [i for i in map(lambda v:v.text, arr)]

        def rate(page: object):
            """Get rating points from a rating bar."""
            rating_bar = re.search(
                r'[■□]{10}　(\d+)', page.get_text()
            )
            return (int(rating_bar.group(1) if not not rating_bar else 0))

        def convert_product_from_aff(link: str) -> str:
            """Convert an affiliated link into a raw link."""
            product_path = 'work/=/product_'
            link = link.replace(
                'dlaf/=/t/i/link/work/aid/momonoyu/', product_path)
            link = link.replace(
                'dlaf/=/link/work/aid/momonoyu/', product_path)
            return link.replace('doonroom-001/', '')

        print(path, end="\r")
        bs = BS(open(path, 'r'), 'lxml')
        pages = bs.find_all(
            'article', attrs={"itemtype": "http://schema.org/BlogPosting"})

        ext_page_data = []
        for page in pages:
            data = {}

            data['page_id'] = int(re.findall(r'\d+', page.h1.a['href'])[0])

            data['article_link'] = page.h1.a['href']

            data['post_date'] = int(datetime.datetime.fromisoformat(
                page.time['datetime']
            ).timestamp())

            data['title'] = page.h1.a.text

            data['body'] = page.select_one('div.article-body-inner').get_text()

            data['rating'] = rate(page)

            data['page_category'] = page.find_all(
                'dd', class_='article-category1'
            )[-1].text

            data['buy_links'] = list(set(
                [convert_product_from_aff(i)
                 for i in map(
                    lambda v: v['href'], page.find_all('a', href=True)
                )
                    if 'doonroom.blog.jp' not in i]
            ))

            data['tags'] = ext_text_from_array(page.dl.find_all('a'))

            data['type'] = self.category

            ext_page_data.append(data)

        return ext_page_data
