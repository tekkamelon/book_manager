#!/bin/sh

# 環境変数設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

set -eu

CSV_FILE="/home/tekkamelon/Documents/github/book_manager/data/library/library.csv"
SCRIPT_DIR="/home/tekkamelon/Documents/github/book_manager"
export PATH="${SCRIPT_DIR}/bin:${PATH}"

printf 'Content-Type: text/html; charset=UTF-8\r\n\r\n'

# CGI POSTデータからq抽出 (dd+tr/cutでPOSIX準拠)
q=""
if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then
  postdata=$(dd bs=1 count="${CONTENT_LENGTH}" 2>/dev/null < /dev/stdin || :)
  q=$(printf '%s' "$postdata" | tr '&' '\n' | grep '^q=' | cut -d= -f2- | urldecode)
fi

cat << EOF
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>検索結果 - Book Manager</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <h1>書籍検索結果</h1>
  <p><a href="../html/search.html">検索</a> | <a href="../html/index.html">メニュー</a></p>
EOF

if [ -n "$q" ]; then
  printf '<p><strong>検索ワード: %s</strong></p>\n' "$(printf '%s' "$q" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')"

  # grep -F でCSV検索しテーブル出力 (全フィールド固定文字列検索)
  grep -F "$q" "$CSV_FILE" | c2h -v header=no
else
  echo '<p class="result">検索ワードを入力してください。</p>'
fi

cat << EOF
  </body>
</html>
EOF
