from __future__ import annotations

import os
import shutil
import urllib.request

from bs4 import BeautifulSoup as BS


class Download(object):
    def __init__(self, category: str, root: str) -> None:
        """Init."""
        self.category = category
        self.save_dir = os.path.join(".", self.category)
        self.root = root

    def get_all_pages(self) -> None:
        """Get pages till a page without an article is shown."""
        shutil.rmtree(self.save_dir, ignore_errors=True)
        os.makedirs(self.save_dir, exist_ok=True)

        for pagenation in range(0, 1000):
            if pagenation == 1:
                continue

            page_param = "?p={}".format(pagenation)
            filename = self.root[(self.root.rfind("/") + 1) :] + page_param
            url = self.root + page_param
            print(url, end="\r")

            if url.lower().startswith("http"):
                req = urllib.request.Request(url)
            else:
                raise ValueError from None

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                source = response.read().decode("utf-8")

            if self.__check_article_exist(source):
                self.__save_file(source, filename)
            else:
                break

        print(" " * 30, end="\r")

    @staticmethod
    def __check_article_exist(source: str) -> bool:
        """Judge if articles exists in a source."""
        articles = BS(source, "lxml").find_all(
            "article", attrs={"itemtype": "http://schema.org/BlogPosting"}
        )
        return len(articles) != 0

    def __save_file(self, source: str, filename: str) -> None:
        """Save source as a file."""
        print(source, file=open(os.path.join(self.save_dir, filename), "w"))
