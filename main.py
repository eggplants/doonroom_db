from glob import glob
import os
from doon_parser.parser import Parser
from doon_parser.database import DoonDatabase
from typing import List
from typing import Callable


def get_filepaths(dir: str) -> List[str]:
    ext_num: Callable[str] = lambda value: int(
        value[-3:].replace('p', '').replace('=', ''))
    return sorted(glob(os.path.join('.', dir, '*')), key=ext_num)


def main() -> None:
    parsed_data = []
    for category in ('dojin', 'hypno'):
        print(' ' * 25, end='\r')
        parser = Parser(category)
        for path in get_filepaths(category):
            parsed_data.extend(parser.execute(path))

    DoonDatabase('doonroom.db').push(parsed_data)


if __name__ == '__main__':
    main()
