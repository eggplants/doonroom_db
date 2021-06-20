from sqlite3 import Error, connect
from typing import Any, Callable, List

from .parser import DatasDict


class DoonDatabase(object):
    def __init__(self, db_filepath: str) -> None:
        """Init."""
        self.db_filepath = db_filepath
        self.log = open('log', 'w')
        self.init_database()

    def init_database(self) -> None:
        """Create a db file and tables if not exists."""
        connect(self.db_filepath)
        self.create_tables()

    def connect_db(self, sql: str,
                   p: List[Any] = [tuple()]) -> None:
        """Connect to the database and execute the SQL."""
        conn = None
        try:
            conn = connect(self.db_filepath)
            call_func: Callable[[str], None] = lambda _:\
                print(_, file=self.log)
            conn.set_trace_callback(call_func)

            c = conn.cursor()
            if not p:
                c.execute(sql)
            else:
                c.executemany(sql, p)

            conn.commit()
        except Error as e:
            print(e)
            import sys
            print(p, file=sys.stderr)
        finally:
            if conn:
                conn.close()

    def create_tables(self) -> None:
        """Create the tables."""
        create_table: Callable[[str], None] = lambda schema:\
            self.connect_db('create table ' + schema)

        create_table(
            '''page (
                    page_id integer,
                    article_link text,
                    post_date integer,
                    title text,
                    body text,
                    rating integer,
                    category text,
                    type text
                ) ''')
        create_table(
            '''link (
                    page_id integer,
                    buy_link text,
                    type text
                ) ''')
        create_table(
            '''tag (
                    page_id integer,
                    tag text
                ) ''')
        create_table(
            '''play (
                    page_id integer,
                    play text
                ) ''')

    def push(self, datas: List[DatasDict]) -> None:
        """Insert data to the database."""
        page_data, link_data, tag_data, play_data = [], [], [], []
        categorize_link: Callable[[str], str] = lambda link: \
            'dlsite' if 'dlsite' in link \
            else 'dmm' if 'dmm' in link \
            else 'other'
        for data in datas:
            page_data.append(
                (
                    data['page_id'],
                    data['article_link'],
                    data['post_date'],
                    data['title'],
                    data['body'],
                    data['rating'],
                    data['category'],
                    data['type']))
            link_data.extend(
                [((data['page_id'], link, categorize_link(link)))
                 for link in data['buy_links']])
            tag_data.extend(
                [(data['page_id'], tag) for tag in data['tags']])
            play_data.extend(
                [(data['page_id'], play) for play in data['plays']])

        self.connect_db(
            'insert into page values (?,?,?,?,?,?,?,?)', page_data)
        self.connect_db('insert into link values (?,?,?)', link_data)
        self.connect_db('insert into tag values (?,?)', tag_data)
        self.connect_db('insert into play values (?,?)', play_data)
