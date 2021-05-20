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
			
			# openBDのapiからデータを取得,"/tmp/data.tmp"に一時保存
			curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format > /tmp/data.tmp
			# タイトル
			title=$(cat /tmp/data.tmp | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') && 
		
			# 著者名
			author=$(cat /tmp/data.tmp | grep author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') && 

			# 出版社
			publisher=$(cat /tmp/data.tmp | grep publisher | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') &&

			# 発売日
			pubdate=$(cat /tmp/data.tmp | grep pubdate | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') &&

		# csvファイルに取得した内容を追記,1行目および末尾3行目を表示
		echo "$isbn,$title,$author,$publisher,$pubdate" >> $file ; column -t -s, $file | sed -n '1p' && tail -n -3 $file | column -t -s,
	fi
done
