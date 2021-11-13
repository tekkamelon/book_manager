#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名を引数で指定
	file=$1

	# 引数の有無を確認
	if [ "$1" = "" ]
	then
		file=~/Documents/library/library.csv
	fi

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		read -p "openBD@ISBN > " "isbn"

		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を取得し,カンマ区切りにして追記
		echo -ne "\n" && echo "'https://api.openbd.jp/v1/get?isbn=$isbn&pretty'" | xargs curl -s | grep -e isbn -we title -e publisher -e pubdate -e author | sed 's/^.*"\(.*\)".*$/\1/' | tr "\n" "," | sed "s/,\$/\n/" | tee -a $file | tr "," " " && echo -ne "\n"

	fi
done
