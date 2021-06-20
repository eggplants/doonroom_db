import os
import shutil
import urllib.request
from typing import Callable

from bs4 import BeautifulSoup as BS


class Download(object):
    def __init__(self, category: str, root: str) -> None:
        """Init."""
        self.category = category
        self.save_dir = os.path.join('.', self.category)
        self.root = root

    def get_all_pages(self) -> None:
        """Get pages till a page without an article is shown."""
        # Judge if articles exists in a source.
        chk_article_exist: Callable[[str], bool] = lambda source:\
            not not BS(source, "lxml").find_all(
                'article', attrs={"itemtype": "http://schema.org/BlogPosting"})

        # Save a file.
        save_file: Callable[[str, str], None] = lambda source, filename:\
            print(source,
                  file=open(os.path.join(self.save_dir, filename), 'w'))

        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

        for pagenation in range(0, 1000):
            if pagenation == 1:
                continue

            page_param = '?p={}'.format(pagenation)
            filename = self.root[(self.root.rfind('/') + 1):] + page_param
            get_url = self.root + page_param
            print(get_url, end="\r")
            fid = urllib.request.urlopen(get_url)
            source = fid.read().decode('utf-8')
            if chk_article_exist(source):
                save_file(source, filename)
            else:
                break

        print(' ' * 30, end='\r')
