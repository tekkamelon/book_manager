# CSV一覧表示機能 コーディング手順書

## 概要

既存の蔵書管理システムにCSVデータの一覧表示機能を追加する。
一覧件数が多くなることを考慮し、既存の検索ページとは独立した新規ページとして実装する。

## 前提

- ブラウザからのリクエストを受け付けるHTTPサーバが起動していること
- CSS等は既存のパス (`../css/style.css`) を参照する
- CGIは従来通り `../cgi-bin/list.cgi` に配置する
- 既存のナビゲーションリンクに、新ページへの導線を追加する必要がある
- プロジェクトルート: `/home/tekkamelon/Documents/github/book_manager`

## 手順

### 1. `html/list.html` を新規作成

- `html/search.html` をテンプレートとして元にし、以下を改変する
- `<title>` を "蔵書一覧 - Book Manager" とする
- `<h1>` を "蔵書一覧" とする
- `form` タグを削除し、POST送信するUIは不要
- JavaScriptで `../cgi-bin/list.cgi` に対してページ読み込み時にGETリクエストを行い、結果をHTMLテーブルとして表示する処理を追加する
  - `fetch("../cgi-bin/list.cgi")` で結果を取得し、レスポンスを `#result` 領域に `innerHTML` で挿入する
  - ローディング表示として `<p>データを読み込んでいます...</p>` を初期表示とする
- 開発者がテスト時に直接CGIを叩けるよう、ページ内に `<a href="../cgi-bin/list.cgi">CGI直接表示</a>` も配置する
- `nav` 内のリンクは他HTMLと同じ構成とする
- `script src="../js/settings.js"` は必要に応じて残す（一覧表示自体には不要だがページ構成の統一のため残しても良い）

### 2. `cgi-bin/list.cgi` を新規作成

- `cgi-bin/search.cgi` をテンプレートとして元にし、POST処理を削除・改変する
- `REQUEST_METHOD` の判定は不要。常に全件取得ロジックを実行する
- CSVファイルパスは `book_manager.conf` から読み込む（search.cgi と同一方式）
- CSVファイルが存在するか確認し、存在しない場合は `データファイルが見つかりません` と返す
- CSVファイルをそのまま読み込み、1行目をヘッダとしてHTMLテーブルに整形して出力する
  - `c2h` コマンドが利用可能であれば `cat "${csv_file}" | c2h -v header=yes` でそのままHTMLテーブル化する
  - `c2h` が使えない場合は手動で `<table>` タグと `tr`, `th`, `td` を生成する
- HTTPレスポンスヘッダは `Content-Type: text/html; charset=UTF-8` とする
- `echo` によるHTML部はsearch.cgiと同様に here-document を用いる
- ナビゲーションリンクを含むHTML構造はsearch.cgiと同じ構成とする

### 3. 既存HTMLに一覧ページへのリンクを追加

以下のファイルすべての `nav` または `.button-group` 内に一覧ページへのリンクを追加する。
なお、追加位置は既存のリンクの並びの「蔵書検索」の直後とする。

対象ファイル:

- `html/index.html`
  - `.button-group` 内に `<button onclick="location.href='list.html'">蔵書一覧</button>` を追加
- `html/search.html`
  - 既存の `nav` 内に `<a href="list.html">蔵書一覧</a>` を追加
- `html/add.html`
  - 既存の `nav` 内に `<a href="list.html">蔵書一覧</a>` を追加
- `html/confirm.html`
  - 既存の `nav` 内に `<a href="list.html">蔵書一覧</a>` を追加
- `html/settings.html`
  - 既存の `nav` 内に `<a href="list.html">蔵書一覧</a>` を追加

### 4. CSS の調整（必要に応じて）

- `css/style.css` にテーブル表示用のスタイルが不足している場合は追記する
  - テーブル幅100%・横スクロール対応（`.scroll-table` 等）
  - `th` の背景色、枠線のスタイル調整
- 既存スタイルと競合しないよう、新規class名を用いて追記する

### 5. テスト手順

1. `http://localhost/html/list.html` にアクセスする
2. ローディング後にHTMLテーブルとしてCSVの内容が表示されることを確認する
3. `CGI直接表示` のリンクから `list.cgi` にアクセスし、HTMLテーブルがそのまま表示されることを確認する
4. 各既存ページから一覧ページへのリンクが正常に遷移することを確認する

## 注意事項

- 既存の `search.cgi` に引き続きPOST検索機能を残したまま、新規の `list.cgi` は独立して動作させる
- シェルスクリプトはPOSIX準拠を維持し、bashismは使用しない
- `cgi-bin/list.cgi` には実行権限 (`chmod +x`) を付与する
- CSVが空（ヘッダのみ）の場合は「蔵書データがありません」と表示するよう考慮する
