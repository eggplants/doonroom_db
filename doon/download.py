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

    def get_all_pages(self) -> bool:
        """Get pages till a page without an article is shown."""

        def chk_article_exist(source: str) -> bool:
            """Judge if articles exists in a source."""
            return not not BS(source, "lxml").find_all(
                'article', attrs={"itemtype": "http://schema.org/BlogPosting"}
            )

        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

        for pagenation in range(0, 1000):
            if pagenation == 1:
                continue

            filename = self.root[(self.root.rfind('/') + 1):] + \
                '?p={}'.format(pagenation)
            get_url = self.root + '?p={}'.format(pagenation)
            print(get_url, end="\r")
            fid = urllib.request.urlopen(get_url)
            source = fid.read().decode('utf-8')

            if chk_article_exist(source):
                f = open(os.path.join(self.save_dir, filename), 'w')
                f.write(source)
                f.close()
            else:
                return True
