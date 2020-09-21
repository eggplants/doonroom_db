from sqlite3 import connect, Error
from typing import List, Any, Callable


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

    def connect_db(self, db_file: str, sql: str, params: tuple = ('')) -> None:
        """Connect to the database and execute the SQL."""
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
        """Create the tables."""
        create_table: Callable[[List[str]], None] = lambda schema:\
            self.connect_db(self.db_filepath, 'create table ' + schema)

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
                ) '''
        )
        create_table(
            '''link (
                    page_id integer,
                    buy_link text,
                    type text
                ) '''
        )
        create_table(
            '''tag (
                    page_id integer,
                    tag text
                ) '''
        )

    def push(self, datas: List[dict]) -> None:
        """Insert data to the database."""
        # Make array elms unique.
        uniq: Callable[[List[Any]], List[Any]] = lambda arr:\
            list(set(arr))

        page_data, link_data, tag_data = [], [], []
        for data in datas:
            page_data.append(
                (data['page_id'], data['article_link'],
                 data['post_date'], data['title'], data['body'],
                 data['rating'],
                 data['page_category'], data['type'])
            )
            link_data.extend(
                [(data['page_id'], link, (
                    'dlsite' if 'dlsite' in link else
                    'dmm' if 'dmm' in link else 'other'))
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
