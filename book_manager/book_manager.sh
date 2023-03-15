#!/bin/sh

# 環境変数の設定
export LANG=C

while :
do

	# ====== 変数の処理 ======
	# 保存先のディレクトリ,ファイル名を引数で指定
	file="${1}"

	# パイプを素通りする"cat"を代入
	cat_tee="cat - "

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

		# 真の場合は"tee"を代入
		cat_tee="tee -a ${file}"

		# 何もしない
		command_exit=":"

	else

		# 偽の場合は何もしない
		:

	fi
	# ====== 変数の処理の終了 ======

	# プロンプトを表示して入力を読み取る 
	printf 'openBD@ISBN > ' && read isbn

	# 空白行を出力
	echo "" &&
	
	# wgetがシステム内に存在するかを確認
	if type wget > /dev/null 2>&1 ; then

		# wgetでapiを叩く
		wget -q -O - "https://api.openbd.jp/v1/get?isbn=${isbn}&pretty"

	# curlがシステム内に存在するかを確認
	elif type curl > /dev/null 2>&1 ; then
		
		# curlでapiを叩く
		curl -s "https://api.openbd.jp/v1/get?isbn=${isbn}&pretty"

	fi |

	# isbn,タイトル,出版社,発売日,著者を抽出
	grep -w -e "isbn" -e "title" -e "publisher" -e "pubdate" -e "author" |

	# 区切り文字にダブルクォートを指定,4フィールド目を出力
	cut -d\" -f4 |

	# 各行をカンマ区切りで1行に結合
	paste -s -d"," |

	# 引数がない場合は"cat",ある場合は"tee"で書き込み
	${cat_tee} |

	# 整形して出力
	tr "," " " 

	# 空白行を出力
	echo "" 

	# 引数がない場合は終了,ある場合は何もしない
	${command_exit}

done

