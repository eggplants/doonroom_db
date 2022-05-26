# doonroom_db

[![PyPI version](
  https://badge.fury.io/py/doonroom-db.svg
)](
  https://badge.fury.io/py/doonroom-db
)

[![release](
  https://github.com/eggplants/doonroom_db/actions/workflows/release.yml/badge.svg
  )](
  https://github.com/eggplants/doonroom_db/actions/workflows/release.yml
) [![DB scheduled release](
  https://github.com/eggplants/doonroom_db/actions/workflows/db_scheduled_release.yml/badge.svg
  )](
  https://github.com/eggplants/doonroom_db/actions/workflows/db_scheduled_release.yml
)

[![Maintainability](
  https://api.codeclimate.com/v1/badges/aa5bc7bb4dbc9209ab8e/maintainability
  )](
  https://codeclimate.com/github/eggplants/doonroom_db/maintainability
) [![pre-commit.ci status](
  https://results.pre-commit.ci/badge/github/eggplants/doonroom_db/master.svg
  )](
  https://results.pre-commit.ci/latest/github/eggplants/doonroom_db/master
)

- A Building Tool for [同人音声の部屋] Unofficial DB
- Separate table for each category in DB
  - [同人音声] (Dojin Voice) and [催眠音声] (Hypno Voice)

[同人音声の部屋]: http://doonroom.blog.jp/
[同人音声]: http://doonroom.blog.jp/archives/cat_966405.html
[催眠音声]: http://doonroom.blog.jp/archives/cat_966995.html

## Install

```bash
pip install doonroom-db
```

## Build DB

```shellsession
$ ddb
Download pages? >> y
...
```

## Log

`log`: issued sql statements are written

## SQL Schema (SQLite3)

```sql
page {
  page_id integer,
  article_link text,
  post_date text,
  title text,
  body text,
  rating integer, -- `99` when the page is unrated
  category text,
  type text -- [dojin|hypno|other]
}

link {
  page_id integer,
  buy_link text,
  type text -- [dlsite|fanza|other]
}
tag {
  page_id integer,
  tag text
}
play {
  page_id integer,
  play text
}
```
