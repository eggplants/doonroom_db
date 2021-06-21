# doonroom_db

[![DB scheduled release](https://github.com/eggplants/doonroom_db/workflows/DB%20scheduled%20release/badge.svg)](https://github.com/eggplants/doonroom_db/actions/runs/366247751) [![release]](https://github.com/eggplants/doonroom_db/actions?query=workflow%3Arelease) [![test]](https://github.com/eggplants/doonroom_db/actions?query=workflow%3Atest) [![Codacy Badge]](https://www.codacy.com/manual/eggplants/doonroom_db?utm_source=github.com&utm_medium=referral&utm_content=eggplants/doonroom_db&utm_campaign=Badge_Grade) [![Maintainability]](https://codeclimate.com/github/eggplants/doonroom_db/maintainability)

[![PyPI version](https://badge.fury.io/py/doonroom-db.svg)](https://badge.fury.io/py/doonroom-db)

- [同人音声の部屋]DB 化

## 概要

- [同人音声の部屋]を DB に入れて検索性を良くする
  - カテゴリ[同人音声]と[催眠音声]を取得
  - パースしてカテゴリごとのテーブルに格納

## DB 作成

```bash
# ページ取得 && パース && DB作成
$ python main.py
Download pages? >> # "y"入力しEnterでページ新規取得
```

## ログ

- `log`
  - 発行した SQL

## スキーマ

- [同人音声], [催眠音声]共通

```sql
page {
  page_id integer,
  article_link text,
  post_date text,
  title text,
  body text,
  rating integer, -- 点数の無い記事（無料作品など）は99を代入
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

[maintainability]: https://api.codeclimate.com/v1/badges/aa5bc7bb4dbc9209ab8e/maintainability
[codacy badge]: https://app.codacy.com/project/badge/Grade/26640885e35e482883b3119ef2fb6380
[test]: https://github.com/eggplants/doonroom_db/workflows/test/badge.svg
[release]: https://github.com/eggplants/doonroom_db/workflows/release/badge.svg
[同人音声の部屋]: http://doonroom.blog.jp/
[同人音声]: http://doonroom.blog.jp/archives/cat_966405.html
[催眠音声]: http://doonroom.blog.jp/archives/cat_966995.html
