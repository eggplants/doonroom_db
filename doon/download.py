import shutil
import os
import urllib.request
from bs4 import BeautifulSoup as BS


class Download(object):
    def __init__(self, category: str, root: str) -> None:
        self.category = category
        self.save_dir = os.path.join('.', self.category)
        self.root = root

    def get_page(self, url: str) -> str:
        print(url, end="\r")
        fid = urllib.request.urlopen(url)
        return fid.read().decode('utf-8')

    def url_basename(self, url: str) -> str:
        return url[(url.rfind('/') + 1):]

    def chk_article_exist(self, source: str) -> bool:
        return not not BS(source, "lxml").find_all(
            'article', attrs={"itemtype": "http://schema.org/BlogPosting"})

    def get_all_pages(self) -> bool:
        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

        pagenation = -1
        while True:
            pagenation += 1
            if pagenation == 1:
                continue

            filename = self.url_basename(
                self.root) + '?p={}'.format(pagenation)
            get_url = self.root + '?p={}'.format(pagenation)
            source = self.get_page(get_url)

            if self.chk_article_exist(source):
                with open(os.path.join(self.save_dir, filename), 'w') as f:
                    f.write(source)
            else:
                return True
