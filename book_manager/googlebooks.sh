#!/bin/bash

tmpfile=/tmp/gbtmp.json

read -p "google books@ISBN > " "isbn"

curl -s https://www.googleapis.com/books/v1/volumes?q=isbn:$isbn > $tmpfile && cat $tmpfile | jq '.items[0] | .volumeInfo | .authors ' | grep -e '\"' | sed 's/"//g'
