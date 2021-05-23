#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名
	file=~/Documents/library/library.csv

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		read -p "ISBN > " "isbn"

		# json形式を整形して出力
		json_format=$(echo "\&pretty")

		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を取得し,カンマ区切りにして追記
		echo -n -e "\n" && curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep -e isbn -e title -e publisher -e pubdate -e author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed -z -e 's/\n/,/g' -e "s/,\$/\n/" | tee -a $file | column -t -s, && echo -n -e "\n"

	fi
done
