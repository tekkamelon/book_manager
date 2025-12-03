#!/bin/sh

# 環境変数設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

set -eu

# テスト用にハードコード
csv_file="/home/tekkamelon/Documents/github/book_manager/data/library/library.csv"
script_dir="/home/tekkamelon/Documents/github/book_manager"
export PATH="${script_dir}/bin:${PATH}"

printf 'Content-Type: text/html; charset=UTF-8\r\n\r\n'

# CGI POSTデータからisbn抽出 (dd+tr/cutでPOSIX準拠)
isbn=""

if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	postdata=$(dd bs=1 count="${CONTENT_LENGTH}" 2>/dev/null < /dev/stdin || :)
	isbn=$(printf '%s' "${postdata}" | tr '&' '\n' | grep '^isbn=' | cut -d'=' -f2- | urldecode)

fi

cat << EOF
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<title>追加結果 - Book Manager</title>
	<link rel="stylesheet" href="../css/style.css">
</head>
<body>
	<h1>書籍追加結果</h1>
	<p><a href="../html/search.html">検索</a> | <a href="../html/add.html">追加</a> | <a href="../html/index.html">メニュー</a></p>
EOF

if [ -z "${isbn}" ]; then

	echo '<p class="result">ISBNを入力してください。</p>'

elif ! echo "${isbn}" | isbn_checker.py >/dev/null 2>&1; then

	printf '<p class="result">無効なISBN: %s</p>\n' "$(printf '%s' "$isbn" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

else

	# bm_search実行 (フォールバック有効)
	data=$(echo "${isbn}" | bm_search -f 2>/dev/null || echo "")

	if [ -z "${data}" ]; then

	printf '<p class="result">書籍情報が見つかりませんでした: %s</p>\n' "$(printf '%s' "$isbn" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"

	else

		# library.csvに追記 (最後の行のみ、CSV形式確認)
		last_line=$(echo "${data}" | tail -1)

		if echo "${last_line}" | grep -q '^[^,]*,[^,]*,'; then

			echo "${last_line}" >> "${csv_file}"

			printf '<p class="result">成功: %s を追加しました。</p>\n' "$(printf '%s' "$isbn" | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g')"
		  
			# 追加データをテーブル表示 (CSVパース)
			echo '<table><thead><tr><th>ISBN</th><th>タイトル</th><th>出版社</th><th>発売日</th><th>著者</th></tr></thead><tbody>'

			echo "${last_line}" | tr ',' '\n' | awk '

				NR==1 { isbn=$0 }
				NR==2 { title=$0 }
				NR==3 { publisher=$0 }
				NR==4 { pubdate=$0 }
				NR==5 { author=$0; printf "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>", isbn, title, publisher, pubdate, author }

			' | sed 's/&/\&amp;/g;s/</\</g;s/>/\>/g'

			echo '</tbody></table>'

		else

			echo '<p class="result">無効なデータ形式です。</p>'

		fi

	fi

fi

cat << EOF
	</body>
</html>
EOF

