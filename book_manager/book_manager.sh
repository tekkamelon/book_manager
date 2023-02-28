#!/bin/sh

# 環境変数の設定
export LANG=C

while :
do

	# 保存先のディレクトリ,ファイル名を引数で指定
	file=$1

	# 引数の有無を確認,あれば真,無ければ偽
	if [ -z "$1" ] ; then

		# 真の場合はプロンプトを表示して入力を読み取る 
		printf 'openBD@ISBN > ' && read isbn

		# 空白行を出力
		echo "" &&
		
		# wgetがシステム内に存在するかを確認
		if type wget > /dev/null 2>&1 ; then

			# wgetでapiを叩く
			wget -q -O - "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		# curlがシステム内に存在するかを確認
		elif type curl > /dev/null 2>&1 ; then
			
			# curlでapiを叩く
			curl -s "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		fi |

		# isbn,タイトル,出版社,発売日,著者を抽出
		grep -w -e "isbn" -e "title" -e "publisher" -e "pubdate" -e "author" |

		# awkで区切り文字をダブルクォートに指定,改行をカンマに置換し4フィールド目を出力
		awk -F\" 'BEGIN{ORS = ","} {print $4}' |

		# 行末のカンマを改行に置換
		sed "s/,\$/\n/" |

		# 整形して出力
		tr "," " " 

		# 空白行を出力
		echo "" 
		
		# 終了する
		exit 0

	# 偽の場合は引数が"Q"の場合に真,それ以外で偽
	elif [ "$isbn" = "Q" ]; then
		
		# メッセージを表示
		echo "finish input" 1>&2
		break

	else

		# 偽の場合はプロンプトを表示して入力を読み取る 
		printf 'openBD@ISBN > ' && read isbn

		# 空白行を出力
		echo "" &&
		
		# wgetがシステム内に存在するかを確認
		if type wget > /dev/null 2>&1 ; then

			# wgetでapiを叩く
			wget -q -O - "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		# curlがシステム内に存在するかを確認
		elif type curl > /dev/null 2>&1 ; then
			
			# curlでapiを叩く
			curl -s "https://api.openbd.jp/v1/get?isbn=$isbn&pretty"

		fi |

		# isbn,タイトル,出版社,発売日,著者を抽出
		grep -w -e "isbn" -e "title" -e "publisher" -e "pubdate" -e "author" |

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

