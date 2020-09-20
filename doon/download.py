import shutil
import os
import urllib.request
from bs4 import BeautifulSoup as BS


class Download(object):
    def __init__(self, category: str, root: str) -> None:
        """Init."""
        self.category = category
        self.save_dir = os.path.join('.', self.category)
        self.root = root

    def get_page(self, url: str) -> str:
        """Return a page source of a given url."""
        print(url, end="\r")
        fid = urllib.request.urlopen(url)
        return fid.read().decode('utf-8')

    def url_basename(self, url: str) -> str:
        """Return the basename of a given url."""
        return url[(url.rfind('/') + 1):]

    def chk_article_exist(self, source: str) -> bool:
        """Judge if articles exists in a source."""
        return not not BS(source, "lxml").find_all(
            'article', attrs={"itemtype": "http://schema.org/BlogPosting"})

    def get_all_pages(self) -> bool:
        """Get pages till a page without an article is shown."""
        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

        for pagenation in range(0, 1000):
            if pagenation == 1:
                continue

            filename = self.url_basename(
                self.root) + '?p={}'.format(pagenation)
            get_url = self.root + '?p={}'.format(pagenation)
            source = self.get_page(get_url)

            if self.chk_article_exist(source):
                f = open(os.path.join(self.save_dir, filename), 'w')
                f.write(source)
                f.close()
            else:
                return True
