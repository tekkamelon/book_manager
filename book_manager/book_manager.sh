#!/bin/bash

while :
do
	if [ "$isbn" = "Q" ]; then
		echo "終了します" && sed -i '/Q/d' /tmp/library.csv
		break
	else
		read -p "ISBN > " "isbn"

		json_format=$(echo "\&pretty")
		
			title=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')
			
			author=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

			publisher=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep publisher | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

			pubdate=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep pubdate | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

		echo "$isbn,$title,$author,$publisher,$pubdate" >> /tmp/library.csv ; column -t -s, /tmp/library.csv | sed -n '1p' && tail -n -3 /tmp/library.csv  | column -t -s,
	fi
done
