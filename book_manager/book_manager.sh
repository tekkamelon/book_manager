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

			# 関数の定義
			catdata () {
				cat /tmp/data.tmp | grep $1 | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g'
			}

			# タイトル
			title=$(catdata title)
		
			# 著者名
			author=$(catdata author)

			# 出版社
			publisher=$(catdata publisher)

			# 発売日
			pubdate=$(catdata pubdate)

		# "$file"に取得した内容を追記,1行目および末尾3行目を表示
		echo -n -e "\n" && echo "$isbn,$title,$author,$publisher,$pubdate" >> $file ; column -t -s, $file | sed -n '1p' && tail -n -3 $file | column -t -s, && echo -n -e "\n"
	fi
done
