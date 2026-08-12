#!/bin/sh

# shellcheck disable=SC1090

# エラー時・未定義変数参照時に終了
set -eu

# ====== 環境変数の設定 ======

# ロケールを C に固定
export LC_ALL=C
export LANG=C

# POSIX 準拠モードを有効化
export POSIXLY_CORRECT=1

# ====== 環境変数の設定ここまで ======


# ====== 変数の初期化 ======

# スクリプト配置ディレクトリの取得
script_dir=$(CDPATH="" cd -- "$(dirname "$0")" && pwd)

# プロジェクト固有ツール(bin)を PATH 先頭へ追加
export PATH="${script_dir}/../bin:${PATH}"

# CSV ファイルパス (設定ファイルで上書き)
csv_file=""

# 入力 ISBN
isbn=""

# CSV 追加フラグ (未指定時は no)
add_to_csv="no"

# 設定ファイルのパス
config_file="$(dirname "$0")/../book_manager.conf"

# ====== 変数の初期化ここまで ======


# 設定ファイルからの変数読み込み
. "${config_file}"


# ====== POST データの解析 ======

# POST かつ Content-Length がある場合のみ本文を処理
if [ "${REQUEST_METHOD:-GET}" = "POST" ] && [ -n "${CONTENT_LENGTH:-}" ]; then

	# 標準入力から POST 本文を取得
	cat_post=$(cat)

	# フォーム値 isbn の抽出
	isbn=$(printf '%s' "${cat_post}" | sed 's/.*isbn=\([^&]*\).*/\1/')

	# フォーム値 add_to_csv の抽出
	add_to_csv=$(printf '%s' "${cat_post}" | sed -n 's/.*add_to_csv=\([^&]*\).*/\1/p')

	# 未送信時は CSV 追加なし
	if [ -z "${add_to_csv}" ]; then
		add_to_csv="no"
	fi

fi

# ====== POST データの解析ここまで ======


# ====== 関数の宣言 ======

# bm_search による書籍データ取得
run_bm_search(){

	# フォールバック有効 (-f) で検索。失敗時は空文字
	data=$(echo "${isbn}" | bm_search -f 2>/dev/null || echo "")
	echo "${data}"

}

# bm_cover による書影 HTML 出力
run_bm_cover(){

	# 書影 URL の取得。失敗時は空文字
	cover_url=$(echo "${isbn}" | bm_cover 2>/dev/null || echo "")

	# URL がある場合のみ img 要素を出力
	if [ -n "${cover_url}" ]; then
		printf '<div class="cover-image"><img src="%s" alt="書影" style="max-width:200px;max-height:300px;margin-top:20px;display:block;margin-left:auto;margin-right:auto;box-shadow:0 4px 12px rgba(0,0,0,0.3);border-radius:4px;"></div>\n' "${cover_url}"
	fi

}

# 検索結果に応じた本文 HTML の組み立て
post_proc(){

	# 書籍データの取得
	data=$(run_bm_search)

	# データなし: 未検出メッセージと Google 検索リンク
	if [ -z "${data}" ]; then

		# HTML エスケープ済み ISBN
		safe_isbn=$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')

		# 未検出メッセージ
		printf '<p class="result">書籍情報が見つかりませんでした: %s</p>\n' "${safe_isbn}"

		# Google 検索ページへのリンク
		printf '<p><a href="../html/google_search.html?isbn=%s" class="button">Google で検索</a></p>\n' "${safe_isbn}"

	else

		# 複数行応答時は最終行を採用
		last_line=$(echo "${data}" | tail -1)

		# CSV らしき形式 (カンマ区切りが2つ以上) の判定
		if echo "${last_line}" | grep -q '^[^,]*,[^,]*,'; then

			# HTML エスケープ済み ISBN
			safe_isbn=$(printf '%s' "${isbn}" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')

			# CSV への追記または取得のみ
			if [ "${add_to_csv}" = "yes" ]; then

				# 蔵書 CSV への1行追記
				echo "${last_line}" >> "${csv_file}"

				# 追加成功メッセージ
				printf '<p class="result">成功: %s を追加しました</p>\n' "${safe_isbn}"

			else

				# 取得のみ成功メッセージ
				printf '<p class="result">成功: %s の情報を取得しました(CSV追加なし)</p>\n' "${safe_isbn}"

			fi

			# 書影の表示
			run_bm_cover

			# 取得行の HTML テーブル化
			echo "${last_line}" | c2h -v header=no

			# 成功時も Google 検索リンクを表示
			printf '<p><a href="../html/google_search.html?isbn=%s" class="button">Google で検索</a></p>\n' "${safe_isbn}"

		else

			# 想定外フォーマット
			echo '<p class="result">無効なデータ形式です</p>'

		fi

	fi

}

# ====== 関数の宣言ここまで ======


# ====== HTML 出力 ======

# CGI ヘッダ
echo "Content-Type: text/html; charset=UTF-8"
echo ""

# 結果ページ本体 (処理結果は post_proc で埋め込み)
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

	<nav>
		<a href="../html/index.html">トップ</a>
		<a href="../html/search.html">蔵書検索</a>
		<a href="../html/add.html">書籍追加・データ検索</a>
		<a href="../html/confirm.html">編集</a>
		<a href="../html/settings.html">設定</a>
	</nav>
<!-- EOF -->
	$(post_proc)

<!-- cat << EOF -->
	</body>
</html>
EOF

# ====== HTML 出力ここまで ======
