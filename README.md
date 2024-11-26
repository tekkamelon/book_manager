# book_manager
自宅用の簡易的な蔵書管理用スクリプト

## install

```sh
# linux及びmacOS
# githubよりclone
git clone https://github.com/tekkamelon/book_manager

# スクリプトのあるディレクトリへ移動
cd book_manager/bin/

# 実行権限を付与
chmod 755 *

# スクリプトを配置
cp book_manager/bin/* [PATHの通ったディレクトリ]
```

## how to use

### book_manager,book_manager_ndl
```sh
# 保存先を引数としてスクリプトを起動,book_manager_ndlも同様
book_manager [保存先のディレクトリ,ファイル名]
```

ISBNを入力すると前者は`bm_core`,後者は`bm_core_ndl`を使用しデータを取得,  
第1引数に指定されたファイルに  
"ISBN,タイトル,著者名,出版社,発売日"の形式で保存  
引数がない場合はデータの出力のみ
"shift+q"を入力で終了

### isbn_checker,isbn_checker.py
```sh
# パイプでISBNコードを渡す
echo "9782379890062" | isbn_checker

echo "9782379890062" | isbn_checker.py
```

パイプで渡されたISBNを検算,正しければそのまま出力,間違っていればエラーメッセージを出力しエラー終了

### csrch
```sh
# 検索するファイルを引数として起動
csrch ~/hoge/fuga.csv

# 検索するワードを入力
search word:

# 検索結果が出力
```
