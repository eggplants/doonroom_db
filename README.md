# doonroom_db

* [同人音声の部屋]DB化

## 概要

* [同人音声の部屋]をDBに入れて検索性を良くする
  * カテゴリ[同人音声]と[催眠音声]を取得
  * パースしてカテゴリごとのテーブルに格納

## 必要

* `python -m pip install bs4`

## DB作成

```bash
# ページ取得
$ LANG= date
Sun Sep 20 14:27:16 JST 2020
$ curl -O 'http://doonroom.blog.jp/archives/cat_966405.html?p=[0-180]'
$ mkdir dojin; mv cat_966405* dojin
$ curl --create-dirs -O 'http://doonroom.blog.jp/archives/cat_966995.html?p=[0-99]'
$ mkdir hypno; mv cat_966995* hypno
# パース && DB作成
$ python main.py
```

## ログ

* `skip_rows`
  * 何個か`<article>~</article>`のパースがおかしくなってスキップしたやつを保存

* `log`
  * 発行したSQL

## スキーマ

* [同人音声], [催眠音声]共通

```text
page {
  page_id integer,
  article_link text,
  post_date text,
  title text,
  body text,
  rating integer,
  category text,
  type text (-> [dojin|hypno|other])
}

link {
  page_id integer,
  buy_link text,
  type text (-> [dlsite|fanza|other])
}
tag {
  page_id integer,
  tag text
}
```

## TODO

* 自動更新
* CLI

[同人音声の部屋]: http://doonroom.blog.jp/

[同人音声]: http://doonroom.blog.jp/archives/cat_966405.html

[催眠音声]: http://doonroom.blog.jp/archives/cat_966995.html
