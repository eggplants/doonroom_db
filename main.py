from glob import glob
import os
from doon_parser.parser import Parser
from doon_parser.database import DoonDatabase
from typing import List

# import pprint


def get_filepaths(dir) -> List[str]:
    def ext_num(value):
        return int(value[-3:].replace('p', '').replace('=', ''))
    return sorted(glob(os.path.join('.', dir, '*=0')), key=ext_num)


def main() -> None:
    # dojin_parsed_data = []
    # dojin_parser = Parser('dojin')
    # for path in get_filepaths('dojin'):
    #     dojin_parsed_data.extend(dojin_parser.execute(path))

    hypno_parsed_data = []
    hypno_parser = Parser('hypno')
    for path in get_filepaths('hypno'):
        hypno_parsed_data.extend(hypno_parser.execute(path))

    DoonDatabase('test.db', hypno_parsed_data, '')


if __name__ == '__main__':
    # pprint(main())
    main()
