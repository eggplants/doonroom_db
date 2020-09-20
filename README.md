# doonroom_db

[![Codacy Badge]](https://www.codacy.com/manual/eggplants/doonroom_db?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eggplants/doonroom_db&amp;utm_campaign=Badge_Grade) [![Maintainability]](https://codeclimate.com/github/eggplants/doonroom_db/maintainability)

* [同人音声の部屋]DB化

## 概要

* [同人音声の部屋]をDBに入れて検索性を良くする
  * カテゴリ[同人音声]と[催眠音声]を取得
  * パースしてカテゴリごとのテーブルに格納

## 必要

* `python -m pip install bs4 lxml`

## DB作成

```bash
# ページ取得 && パース && DB作成
$ python main.py
Download pages? >> # "y"入力しEnterでページ新規取得
```

## ログ

* `log`
  * 発行したSQL

## スキーマ

* [同人音声], [催眠音声]共通

```sql
page {
  page_id integer,
  article_link text,
  post_date text,
  title text,
  body text,
  rating integer, -- 点数の無い記事は0を代入
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
```

## TODO

* [ ] 検索UI
  * [ ] CLI
  * [ ] GUI

[Maintainability]: https://api.codeclimate.com/v1/badges/aa5bc7bb4dbc9209ab8e/maintainability

[Codacy Badge]: https://app.codacy.com/project/badge/Grade/26640885e35e482883b3119ef2fb6380

[同人音声の部屋]: http://doonroom.blog.jp/

[同人音声]: http://doonroom.blog.jp/archives/cat_966405.html

[催眠音声]: http://doonroom.blog.jp/archives/cat_966995.html
