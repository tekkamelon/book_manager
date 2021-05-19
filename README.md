# book_manager
自宅用の簡易的な蔵書管理用スクリプト

## install

```sh
# githubよりclone
$ git clone https://github.com/tekkamelon/book_manager

# スクリプトのあるディレクトリへ移 
$ cd book_manager/book_manager/

# 実行権限を付与
$ chmod 755 book_manager.sh
```

## hot to use

```sh
# スクリプトを起動
$ ./book_manager.sh
```

ISBNを入力するとopenBDからデータを取得,  
指定したファイル(デフォルトでは"/tmp/library.csv")に  
ISBN,タイトル,著者名,出版社,発売日が入力される.  
終了するときは"shift+q"を入力