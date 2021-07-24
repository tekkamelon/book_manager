# book_manager
自宅用の簡易的な蔵書管理用スクリプト

## install

```sh
# linux及びmacOS
# githubよりclone
$ git clone https://github.com/tekkamelon/book_manager

# スクリプトのあるディレクトリへ移動
$ cd book_manager/book_manager/

# 実行権限を付与
$ chmod 755 book_manager.sh
```

## how to use

```sh
# 保存先を引数としてスクリプトを起動,引数がない場合は"~/Documents/library/library.csv"に保存
$ ./book_manager.sh [保存先のディレクトリ,ファイル名]
```

ISBNを入力するとopenBDからデータを取得,  
"$file"に指定されたファイル(デフォルトでは"~/Documents/library/library.csv")に  
ISBN,タイトル,著者名,出版社,発売日が入力される.  
"shift+q"を入力で終了
