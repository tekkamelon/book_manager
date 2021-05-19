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
			
			# タイトル
			title=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')
		
			# 著者名
			author=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

			# 出版社
			publisher=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep publisher | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

			# 発売日
			pubdate=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep pubdate | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

		# csvファイルに取得した内容を追記,1行目および末尾3行目を表示
		echo "$isbn,$title,$author,$publisher,$pubdate" >> $file ; column -t -s, $file | sed -n '1p' && tail -n -3 $file | column -t -s,
	fi
done
