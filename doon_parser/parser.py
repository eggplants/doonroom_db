import datetime
import re
from typing import List

from bs4.element import Tag
from bs4 import BeautifulSoup as BS


class ParseUnknownCategory(Exception):
    pass


class Parser(object):

    def __init__(self, category: str) -> None:
        self.log = open('skip_works', 'w')
        if category not in ['hypno', 'dojin']:
            raise ParseUnknownCategory("Unknown Category: %s" % self.category)

        self.category = category

    def ext_text_from_array(self, arr: List) -> List[str]:
        return [i for i in map(lambda v:v.text, arr)]

    def convert_product_from_aff(self, link: str) -> str:
        product_path = 'work/=/product_'
        link = link.replace('dlaf/=/t/i/link/work/aid/momonoyu/', product_path)
        link = link.replace('dlaf/=/link/work/aid/momonoyu/', product_path)

        return link.replace('doonroom-001/', '')

    def href_text_from_array(self, arr: List[Tag]) -> List[str]:
        links = [self.convert_product_from_aff(i)
                 for i in map(lambda v: v['href'], arr)
                 if 'doonroom.blog.jp' not in i]
        return list(set(links))

    def rate(self, page: object):
        try:
            rating_bar = page.find_all(
                'span', style='font-size: large;', text=re.compile('点')
            )[-1].text
            return int(re.search(r'(\d+)点', rating_bar).group(1))
        except IndexError:
            return 0

    def parse(self, path: str) -> List[dict]:
        print(path, end="\r")
        bs = BS(open(path, 'r'), 'html.parser')
        pages = bs.find_all('article')

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

            data['rating'] = self.rate(page)

            try:
                data['page_category'] = page.find_all(
                    'dd', class_='article-category1'
                )[-1].text
            except IndexError:
                # 何個かarticleのパースがおかしくなるやつがある
                print(page.h1.a.text, page.h1.a['href'], file=self.log)
                continue

            data['buy_links'] = self.href_text_from_array(
                page.find_all('a', href=True))

            data['tags'] = self.ext_text_from_array(page.dl.find_all('a'))

            data['type'] = self.category

            ext_page_data.append(data)

        return ext_page_data

    def execute(self, path: str) -> List:
        return self.parse(path)
