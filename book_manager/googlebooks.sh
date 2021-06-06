#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名
	# file=~/Documents/library/library.csv
	file=/tmp/library.csv

	# 一時保存先のディレクトリ,ファイル名
	tmpfile=/tmp/gbtmp.json

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		read -p "google books@ISBN > " "isbn"

		# google book api よりデータを取得
		curl -s https://www.googleapis.com/books/v1/volumes?q=isbn:$isbn > $tmpfile 

		# タイトル
		title=$(cat $tmpfile | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') && 
		# 出版社
		publisher=$(cat $tmpfile | grep publisher | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') && 

		# 発売日 
		pubdate=$(cat $tmpfile | grep publishedDate | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g') && 

		# 著者名
		author=$(cat $tmpfile | jq '.items[0] | .volumeInfo | .authors ' | grep -e '\"' | sed 's/"//g' | sed 's/,//g') && 

		echo -n -e "\n" && echo "$title,$author,$publisher,$pubdate" >> $file ; column -t -s, $file | sed -n '1p' && tail -n -3 $file | column -t -s, && echo -n -e "\n"

	fi
done
