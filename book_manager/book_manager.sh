read -p "ISBN > " "isbn"

json_format=$(echo "\&pretty")

title=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

author=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn$json_format | grep author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

echo "$isbn,$title,$author" >> /tmp/libary.csv ; column -t -s, /tmp/libary.csv
