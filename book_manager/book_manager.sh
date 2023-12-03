#!/bin/sh

# ====== 環境変数の設定 ======
# 環境変数の設定
export LC_ALL=C
export LANG=C

# GNU coreutilsの挙動をPOSIXに準拠
export POSIXLY_CORRECT=1
# ====== 環境変数の設定ここまで ======


# apiを叩き,結果を加工
hit_api(){

	# wgetがシステム内に存在するかを確認
	if type wget > /dev/null 2>&1 ; then

		# wgetでapiを叩く
		wget -q -O - "https://api.openbd.jp/v1/get?isbn=${isbn}&pretty"

	# curlがシステム内に存在するかを確認
	elif type curl > /dev/null 2>&1 ; then
		
		# curlでapiを叩く
		curl -s "https://api.openbd.jp/v1/get?isbn=${isbn}&pretty"

	else

		# wgetもcurlもない場合はメッセージを表示
		echo 'please install "wget" or "curl"' 1>&2

	fi |

	# isbn,タイトル,出版社,発売日,著者を抽出
	grep -F -w -e "isbn" -e "title" -e "publisher" -e "pubdate" -e "author" |

	# 区切り文字をダブルクォートに指定
	awk -F "\"" '{

		# 行頭が"      "author""にマッチする場合は真,それ以外で偽
		if(/^      "author"/) {

			# 真の場合の処理
			# カンマを削除
			gsub( "," , "" )

			# "西暦-ダブルクォート"の部分を削除
			gsub( /[0-9][0-9][0-9][0-9]-/ , "" )
			
			# "西暦-西暦ダブルクォート"の部分を削除
			gsub( /[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]/ , "" )

			# "末尾が西暦とダブルクォート"の部分を削除
			gsub( /[0-9][0-9][0-9][0-9]\"$/ , "" )
			
			# 4フィールド目を出力
			print $4

		}else{

			# 偽の場合は4フィールド目を出力
			print $4
			
		}

	}' |

	# 区切り文字をカンマに指定,列を行に置換
	paste -s -d ',' -

}

# 標準入力の有無を確認,あれば真,無ければ偽
if [ -p /dev/stdin ] ; then

	# 真の場合は標準入力を変数に代入,非対話的に処理
	isbn=$(cat - )

	# apiを叩く
	"hit_api"

else

	# 偽の場合は対話的に処理
	while :
	do
	

		# ====== 変数の処理 ======
		# 保存先のディレクトリ,ファイル名を引数で指定
		file="${1}"
	
		# 入力が"Q"の場合に真,それ以外で偽
		if [ "${isbn}" = "Q" ] ; then
			
			# メッセージを標準エラー出力に表示
			echo "finish input" 1>&2
	
			# whileのループから脱出
			break
	
		# 偽の場合は引数の有無を確認,無ければ真
		elif [ -z "${file}" ] ; then
	
			# 出力を捨てる
			file="/dev/null"

		fi
		# ====== 変数の処理の終了 ======


		# プロンプトを表示して入力を読み取る 
		printf 'openBD@ISBN > ' && read -r isbn
	
		echo ""
	
		# apiを叩く
		"hit_api" |

		# 空白行を削除
		sed '/^$/d' |

		# 指定ファイルに追記,指定されてない場合は/dev/nullへ
		tee -a "${file}"
	
		echo "" 
	
	done

fi

