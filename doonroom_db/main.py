from __future__ import annotations

import os
from glob import glob

from .database import DoonDatabase
from .download import Download
from .parser import DatasDict, Parser


def get_filepaths(dirpath: str) -> list[str]:
    """Get the file paths in the specified directory."""

    def extract_page_number(v: str) -> int:
        return int(v[-3:].replace("p", "").replace("=", ""))

    return sorted(glob(os.path.join(".", dirpath, "*")), key=extract_page_number)


def main() -> None:
    """Main!!!"""
    if input("Download pages? >> ") == "y":
        Download(
            "dojin", "http://doonroom.blog.jp/archives/cat_966405.html"
        ).get_all_pages()
        Download(
            "hypno", "http://doonroom.blog.jp/archives/cat_966995.html"
        ).get_all_pages()

    parsed_data: list[DatasDict] = []
    for category in ("dojin", "hypno"):
        parser = Parser(category)
        for path in get_filepaths(category):
            dict_data = parser.parse(path)
            parsed_data.extend(dict_data)

    DoonDatabase("doonroom.db").push(parsed_data)


if __name__ == "__main__":
    main()
