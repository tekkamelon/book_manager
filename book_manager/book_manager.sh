#!/bin/sh

# 環境変数の設定
export LC_ALL=C
export LANG=C

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

	# 組み込み変数の設定
	awk 'BEGIN{

		# 区切り文字にダブルクォートに指定
		FS = "\""

		# レコード区切り文字を改行からカンマに指定
		ORS = ","

	}
	
	{

		# 行頭が"      "author""にマッチする場合は真,それ以外で偽
		if(/^      "author"/) {

			# 真の場合の処理
			# カンマを削除
			gsub( "," , "" )

			# "4桁の数字-ダブルクォート"の部分を削除
			gsub( /[0-9][0-9][0-9][0-9]-/ , "" )
			
			# "4桁の数字-4桁の数字ダブルクォート"の部分を削除
			gsub( /[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]/ , "" )

			# 4フィールド目を出力
			print $4

		}else{

			# 偽の場合は4フィールド目を出力
			print $4
			
		}

	}' |

	# 末尾のカンマの削除
	sed "s/,$/\n/g"

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
	
		# 読み込み終了の"exit"を代入
		command_exit="exit 0"
	
		# 入力が"Q"の場合に真,それ以外で偽
		if [ "${isbn}" = "Q" ] ; then
			
			# メッセージを標準エラー出力に表示
			echo "finish input" 1>&2
	
			# whileのループから脱出
			break
	
		# 偽の場合は引数の有無を確認,あれば真,無ければ偽
		elif [ -n "${file}" ] ; then
	
			# 真の場合は何もしないコマンドを代入
			command_exit=":"
	
		else

			# 偽の場合は"file"に"/dev/null"を代入
			file="/dev/null"

		fi
		# ====== 変数の処理の終了 ======

	
		# プロンプトを表示して入力を読み取る 
		printf 'openBD@ISBN > ' && read -r isbn
	
		# 空白行を出力
		echo ""
	
		# apiを叩く
		"hit_api" |

		# 指定ファイルに追記,指定されてない場合は/dev/nullへ
		tee -a "${file}"
	
		# 空白行を出力
		echo "" 
	
		# 引数がない場合は終了,ある場合は何もしない
		${command_exit}
	
	done

fi

