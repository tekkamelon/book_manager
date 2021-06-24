#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名
	file=/tmp/library.csv

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		read -p "openBD@ISBN > " "isbn"

		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を取得し,カンマ区切りにして追記
		echo -ne "\n" && echo "'https://api.openbd.jp/v1/get?isbn=$isbn&pretty'" | xargs curl -s | grep -e isbn -e title -e publisher -e pubdate -e author | grep -v "Subtitle" | sed 's/^.*"\(.*\)".*$/\1/' | sed -ze 's/\n/,/g' -e "s/,\$/\n/" | tee -a $file | column -ts, && echo -ne "\n"

	fi
done
