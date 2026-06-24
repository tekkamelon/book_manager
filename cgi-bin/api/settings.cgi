#!/bin/sh

set -eu

# 環境変数の設定
export LC_ALL=C
export LANG=C
export POSIXLY_CORRECT=1

# 設定ファイルのパス
config_file="$(dirname "$0")/../../book_manager.conf"

# JSONエスケープ用関数
escape_json() {
	printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

# 設定値の初期化
csv_file=""
code_server=""

# 設定ファイルから値を読み込み
if [ -f "${config_file}" ]; then

	csv_file=$(grep '^csv_file=' "${config_file}" | cut -d'=' -f2- | sed 's/^"//;s/"$//')
	code_server=$(grep '^code_server=' "${config_file}" | cut -d'=' -f2- | sed 's/^"//;s/"$//')

fi

# JSONレスポンスを出力
json_csv=$(escape_json "${csv_file}")
json_code=$(escape_json "${code_server}")

echo "Content-Type: application/json; charset=UTF-8"
echo ""
printf '{"csv_file":"%s","code_server":"%s"}\n' "${json_csv}" "${json_code}"
