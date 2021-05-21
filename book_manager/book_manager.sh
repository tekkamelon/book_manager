#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名
	file=/tmp/library.csv

	if [ "$isbn" = "Q" ]; then
		echo "終了します" && sed -i '/Q/d' $file
		break

	else

		# ISBN
		read -p "ISBN > " "isbn"

		# json形式を整形して出力
		json_format=$(echo "\&pretty")

		echo -n -e "\n" ;
		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を取得し,カンマ区切りにして追記
		curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep -e isbn -e title -e author -e publisher -e pubdate | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed -z -e 's/\n/,/g' -e "s/,\$/\n/" >> $file ; cat $file | column -t -s, | sed -n '1p' && tail -n -3 $file | column -t -s, && echo -n -e "\n" 

	fi
done
