#!/usr/bin/awk -f

BEGIN{

	# 1文字ずつフィールドに分割
	FS = ""

}

{

	# カウンタ用変数iを1から13まで2づつ増やす
	for(i = 1; i <= 13; i += 2)

		# 各フィールドを足しodd_numに代入
		odd_num += $i

	# カウンタ用変数iを2から12まで2づつ増やす
	for(i = 2; i <= 12; i += 2)

		# 各フィールドを足しeven_numに代入
		even_num += $i

	# 奇数桁と偶数桁の3倍を合計
	addition = odd_num+even_num * 3

	# 10で割った剰余を求める
	surplus = addition % 10

}

END{

	# 剰余が0なら真,それ以外で偽
	if(surplus == 0){

		# 真の場合は入力内容をそのままを出力
		print $0

	}else{

		# 偽の場合はエラーメッセージを出力
		print "ISBN is bad!" > "/dev/stderr"

	}
	
}

