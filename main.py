from glob import glob
import os
from doon.parser import Parser
from doon.database import DoonDatabase
from doon.download import Download
from typing import List
from typing import Callable


def get_filepaths(dirpath: str) -> List[str]:
    """Get the file paths in the specified directory"""
    ext_num: Callable[str] = lambda value: int(
        value[-3:].replace('p', '').replace('=', ''))
    return sorted(glob(os.path.join('.', dirpath, '*')), key=ext_num)


def main() -> None:
    """Main!!!"""

    if input('Download pages? >> ') == 'y':
        Download(
            'dojin', 'http://doonroom.blog.jp/archives/cat_966405.html'
        ).get_all_pages()
        print(' ' * 25, end='\r')
        Download(
            'hypno', 'http://doonroom.blog.jp/archives/cat_966995.html'
        ).get_all_pages()

    parsed_data = []
    for category in ('dojin', 'hypno'):
        print(' ' * 25, end='\r')
        parser = Parser(category)
        for path in get_filepaths(category):
            parsed_data.extend(parser.parse(path))

    DoonDatabase('doonroom.db').push(parsed_data)


if __name__ == '__main__':
    main()
