from sqlite3 import connect
from sqlite3 import Error
from typing import List
from typing import Any


class DoonDatabase(object):
    def __init__(self, db_filepath: str) -> None:
        self.db_filepath = db_filepath
        self.log = open('log', 'w')
        self.init_database()

    def init_database(self) -> None:
        connect(self.db_filepath)
        self.create_tables()

    def connect_db(self, db_file: str, sql: str, params: tuple = ('')) -> None:
        conn = None
        try:
            conn = connect(db_file)
            conn.set_trace_callback(lambda _: print(_, file=self.log))

            c = conn.cursor()
            if not params:
                c.execute(sql)
            else:
                c.executemany(sql, params)

            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_tables(self) -> None:
        def unko(schemas: List[str]) -> None:
            for schema in schemas:
                self.connect_db(
                    self.db_filepath,
                    'create table ' + schema
                )

        unko([
            '''page (
                    page_id integer,
                    article_link text,
                    post_date integer,
                    title text,
                    body text,
                    rating integer,
                    category text,
                    type text
                ) ''',

            '''link (
                    page_id integer,
                    buy_link text,
                    type text
                ) ''',

            '''tag (
                    page_id integer,
                    tag text
                ) '''
        ])

    def push(self, datas: List[dict]) -> None:
        def type_link(link: str) -> str:
            if 'dlsite' in link:
                return 'dlsite'
            elif 'dmm' in link:
                return 'dmm'
            else:
                return 'other'

        def uniq(arr: List[Any]) -> List[Any]:
            return list(set(arr))
        # page
        page_data, link_data, tag_data = [], [], []
        for data in datas:
            page_data.append(
                (data['page_id'], data['article_link'],
                 data['post_date'], data['title'], data['body'],
                 data['rating'],
                 data['page_category'], data['type'])
            )
            link_data.extend(
                [(data['page_id'], link, type_link(link))
                 for link in data['buy_links']]
            )
            tag_data.extend(
                [(data['page_id'], tag) for tag in data['tags']]
            )

        self.connect_db(
            self.db_filepath,
            'insert into page values (?,?,?,?,?,?,?,?)',
            uniq(page_data)
        )
        self.connect_db(
            self.db_filepath,
            'insert into link values (?,?,?)',
            uniq(link_data)
        )
        self.connect_db(
            self.db_filepath,
            'insert into tag values (?,?)',
            uniq(tag_data)
        )
