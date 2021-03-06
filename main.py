import os
from glob import glob
from typing import Callable, List

from doon.database import DoonDatabase
from doon.download import Download
from doon.parser import DatasDict, Parser


def get_filepaths(dirpath: str) -> List[str]:
    """Get the file paths in the specified directory."""
    ext_num: Callable[[str], int] = lambda value: int(
        value[-3:].replace('p', '').replace('=', ''))
    return sorted(glob(os.path.join('.', dirpath, '*')), key=ext_num)


def main() -> None:
    """Main!!!"""
    if input('Download pages? >> ') == 'y':
        Download(
            'dojin', 'http://doonroom.blog.jp/archives/cat_966405.html'
        ).get_all_pages()
        Download(
            'hypno', 'http://doonroom.blog.jp/archives/cat_966995.html'
        ).get_all_pages()

    parsed_data: List[DatasDict] = []
    for category in ('dojin', 'hypno'):
        parser = Parser(category)
        for path in get_filepaths(category):
            dict_data = parser.parse(path)
            parsed_data.extend(dict_data)

    DoonDatabase('doonroom.db').push(parsed_data)


if __name__ == '__main__':
    main()
