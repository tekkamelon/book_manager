# 書籍追加結果ページからの再検索・再追加 UI

## 目的

`cgi-bin/add.cgi` が返す「書籍追加結果」ページから、`html/add.html` へ戻らずに続けて ISBN 検索および CSV 追加ができるようにする。

現状は結果表示と Google 検索リンクのみで、次の ISBN を扱うにはナビの「書籍追加・データ検索」へ遷移する必要がある。連続追加の手数を減らす。

## 現状

### 入力 (`html/add.html`)

- `POST` 先: `../cgi-bin/add.cgi`
- 項目:
  - ISBN (`name="isbn"`, required)
  - バーコード読取 (`js/barcode.js` + `js/vendor/html5-qrcode.min.js`)
  - CSV 追加トグル (`name="add_to_csv"`, `value="yes"`, 初期 checked)
  - 対象 CSV パス表示 (`js/settings.js` の `loadCsvFilePath`)

### 結果 (`cgi-bin/add.cgi`)

- タイトル: 書籍追加結果
- `post_proc` の出力 (成功/未検出メッセージ、書影、テーブル、Google 検索リンク)
- ナビはあるが、入力フォームは無い
- `container` / `card` が無く、`add.html` とマークアップが揃っていない

## 方針

結果ページの処理結果の下に、`add.html` と同等のフォームを置く。送信先は同じ `add.cgi` とし、結果表示のたびに新しい ISBN を投入できる。

フォーム HTML は `add.html` と `add.cgi` で二重管理になりやすいため、まずは結果ページへ同等マークアップを埋め込み、共通化は必要になった段階で検討する (本計画の必須範囲外)。

## 対象ファイル

| ファイル | 変更内容 |
| --- | --- |
| `cgi-bin/add.cgi` | 結果 HTML にフォーム・スクリプトを追加。レイアウトを `add.html` に近づける |
| `html/add.html` | 原則変更なし (参照実装) |
| `css/style.css` | 既存クラスで足りれば変更なし |
| `js/barcode.js` / `js/settings.js` | 既存 API を再利用。変更なし想定 |
| `tests/` | 結果ページ上の再送信を Playwright で追加 |

## UI 仕様

結果ページの構成 (上から):

1. `h1`: 書籍追加結果 (現状維持)
2. `nav`: 既存ナビ。`aria-current="page"` は書籍追加・データ検索のまま
3. 処理結果 (`post_proc`)
   - メッセージ、書影、テーブル、Google 検索リンク
4. 区切り見出し (例: `h2` 「続けて検索・追加」)
5. フォーム (`card` 内)
   - ISBN 入力 (空欄、前回値は入れない。連続入力時の誤再送信を防ぐ)
   - バーコード読取ボタンとプレビュー領域 (id は `add.html` と同じで可。1ページ1フォーム)
   - CSV 追加トグル (初期 checked。`add.html` と揃える)
   - 対象ファイル表示 (`current_csv_file`)
   - 実行ボタン (`value="実行"`)

パス:

- 結果ページは `cgi-bin/` 配下で出力されるため、相対パスは現状どおり `../html/` `../css/` `../js/`
- フォーム `action` は空または `add.cgi` (同一 CGI への POST)

アクセシビリティ:

- フォームの `label for="isbn"` を維持
- バーコード領域は `hidden` 初期状態
- 結果メッセージとフォームは別ブロックにし、スクリーンリーダで結果が先に読める順にする

## `add.cgi` 実装メモ

- heredoc 内にフォーム HTML を置く。`post_proc` の直後、`</body>` の前
- スクリプトは `add.html` と同様:
  - `../js/settings.js` と `loadCsvFilePath('current_csv_file', ...)`
  - `../js/vendor/html5-qrcode.min.js`
  - `../js/barcode.js` と `mountBarcodeReader({...})`
- heredoc 内の `$` はシェル展開される。JS の `$` は使わない (現状の `add.html` もプレーン JS)
- `$(post_proc)` 以外の `$` / バッククォートは heredoc 終端までエスケープまたは EOF をクォートしない場合に注意
- `container` で全体を包み、結果とフォームの見た目を `add.html` に寄せる

バーコード:

- HTTPS / localhost でないとカメラが使えない点は `add.html` と同じ制約
- 結果ページでも同じ `mountBarcodeReader` を呼ぶ

## 非対象

- 検索結果の一覧化や履歴表示
- フォーム部品のテンプレート共通化
- `add.html` の項目追加・削除
- Google 検索ページへの同様フォーム追加

## テスト計画 (Playwright)

前提 URL: `http://localhost/html/add.html` (明示がなければホスト `localhost`、ポート `80`)

### TC-R001: 結果ページにフォームがある

1. `add.html` で ISBN を投入し実行
2. 書籍追加結果が表示される
3. ISBN 入力、CSV トグル、実行ボタン、対象ファイル表示がある

### TC-R002: 結果ページから再検索 (CSV 追加なし)

1. 結果ページで別 ISBN を入力
2. CSV トグルをオフにして実行
3. 新しい結果メッセージが出る (CSV追加なし)
4. フォームが再度表示される

### TC-R003: 結果ページから再追加 (CSV 追加あり)

1. 結果ページで ISBN を入力しトグルオンで実行
2. 「追加しました」系メッセージが出る

### TC-R004: 未検出後もフォームが使える

1. 存在しない ISBN で実行
2. 未検出メッセージと Google リンクに加え、フォームがある
3. 正しい ISBN を再投入できる

バーコードの実カメラ操作は既存方針に合わせ、本計画では必須としない。フォーム DOM と `barcode-start` の存在確認までとする。

## 実装手順

1. `add.cgi` の結果 HTML に `container` とフォーム、スクリプトを追加
2. heredoc の変数展開漏れ・余分な展開が無いか確認
3. ブラウザで成功・未検出の両経路から連続操作できることを確認
4. Playwright ケースを `tests/` に追加
5. 必要ならナビ欠落 (結果ページに「編集」があり `add.html` に無い等) は本タスクでは触らない

## 完了条件

- 書籍追加結果から、トップや `add.html` に戻らず ISBN 検索・CSV 追加ができる
- バーコード読取 UI が結果ページでも初期化される
- CSV 対象パスが表示される
- 成功・未検出いずれでもフォームが残る
- 既存の結果表示 (書影、テーブル、Google 検索) が壊れない
