#!/bin/sh

while :
do
	# 保存先のディレクトリ,ファイル名を引数で指定
	file=$1

	# 引数の有無を確認
	if [ "$1" = "" ]
	then
		:
	fi

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		echo 'openBD@ISBN > ' | tr "\n" " " && read isbn

		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を抽出し,カンマ区切りにして追記
		echo "" &&
		
		# wgetがなければcurlを使用
		if type wget > /dev/null 2>&1; then
			wget -q -O - "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"
		elif type curl > /dev/null 2>&1; then
			curl -s "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"
		fi |
		grep -E -w "isbn|title|publisher|pubdate|author" |
		awk -F\" 'BEGIN{ORS = ","} {print $4}' |
		sed "s/,\$/\n/" |
		tee -a $file |
		tr "," " " 
		echo "" 
	fi
done
