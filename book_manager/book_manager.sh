read -p "ISBN > " "isbn"

title=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn | jq . | grep title | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle")

author=$(curl -s https://api.openbd.jp/v1/get?isbn=$isbn | jq . | grep author | sed 's/^.*"\(.*\)".*$/\1/' | grep -v "Subtitle" | sed 's/,//g')

echo "$isbn,$title,$author" | tee /tmp/libary.csv
