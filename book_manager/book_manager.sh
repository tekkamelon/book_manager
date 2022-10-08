#!/bin/sh

while :
do
	# 保存先のディレクトリ,ファイル名を引数で指定
	file=$1

	# 引数の有無を確認
	if [ "$1" = "" ]
	then
		:
	fi

	if [ "$isbn" = "Q" ]; then
		echo "入力を終了" 
		break

	else

		# ISBN
		echo 'openBD@ISBN > ' | tr "\n" " " && read isbn

		# openBDからデータを取得,isbn,タイトル,出版社,発売日,著者を抽出し,カンマ区切りにして追記
		echo "" &&
		
		# wgetがシステム内に存在するかを確認
		if type wget > /dev/null 2>&1; then

			# wgetでapiを叩く
			wget -q -O - "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		# curlがシステム内に存在するかを確認
		elif type curl > /dev/null 2>&1; then
			
			# curlでapiを叩く
			curl -s "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		fi |

		# それぞれのフィールドに完全一致する行を抽出
		grep -E -w "isbn|title|publisher|pubdate|author" |

		# awkで区切り文字をダブルクォートに指定,改行をカンマに置換し4フィールド目を出力
		awk -F\" 'BEGIN{ORS = ","} {print $4}' |

		# 行末のカンマを改行に置換
		sed "s/,\$/\n/" |

		# 引数で指定されたファイルに追記
		tee -a $file |

		# 整形して出力
		tr "," " " 

		# 空白行を出力
		echo "" 

	fi
done
