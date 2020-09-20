from glob import glob
import os
from doon.parser import Parser
from doon.database import DoonDatabase
from doon.download import Download
from typing import List
from typing import Callable


def get_filepaths(dir: str) -> List[str]:
    ext_num: Callable[str] = lambda value: int(
        value[-3:].replace('p', '').replace('=', ''))
    return sorted(glob(os.path.join('.', dir, '*')), key=ext_num)


def main() -> None:

    if input('Download pages? >> ') == 'y':
        Download(
            'dojin', 'http://doonroom.blog.jp/archives/cat_966405.html'
        ).get_all_pages()
        Download(
            'hypno', 'http://doonroom.blog.jp/archives/cat_966995.html'
        ).get_all_pages()

    parsed_data = []
    for category in ('dojin', 'hypno'):
        print(' ' * 25, end='\r')
        parser = Parser(category)
        for path in get_filepaths(category):
            parsed_data.extend(parser.execute(path))

    DoonDatabase('doonroom.db').push(parsed_data)


if __name__ == '__main__':
    main()
