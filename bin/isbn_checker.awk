#!/usr/bin/awk -f

BEGIN{

	# 1文字ずつフィールドに分割
	FS=""

}

{

	# 奇数桁を足す
	odd_num=$1+$3+$5+$7+$9+$11+$13

	# 偶数桁を3倍し足す
	even_num=$2*3+$4*3+$6*3+$8*3+$10*3+$12*3

	# 奇数桁と偶数桁を合計
	addition=odd_num+even_num

	# 10で割った剰余を求める
	surplus=addition%10

	# 剰余が0なら真,それ以外で偽
	if (surplus == 0) {

		# 真の場合は環境変数をリセット,入力行を出力
		FS = " "

		print $0

	}else{

		# 偽の場合はエラーメッセージを出力
		print "ISBN is bad!" > "/dev/stderr"

	}

}

