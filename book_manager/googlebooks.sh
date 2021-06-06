#!/bin/bash

while :
do
	# 保存先のディレクトリ,ファイル名
	file=~/Documents/library/library.csv

	# 一時保存先のディレクトリ,ファイル名
	tmpfile=/tmp/gbtmp.json

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		read -p "google books@ISBN > " "isbn"

		# google book apiからデータを取得
		curl -s https://www.googleapis.com/books/v1/volumes?q=isbn:$isbn > $tmpfile && cat $tmpfile | jq '.items[0] | .volumeInfo | .authors ' | grep -e '\"' | sed 's/"//g'

	fi
done
