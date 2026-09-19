# ローカルHTTPSサーバーの例(iPhone実機検証用)

## 概要

`plans/barcode_scan_ios.md`のHTTPS要件に対する、ローカル検証用の手順例。
iOS Safariの`getUserMedia`はセキュアコンテキスト必須のため、
iPhone実機からLAN IPで`http://`接続するとカメラが拒否される。
現状の`cgi_server.py`は`http://127.0.0.1:8000`のHTTPかつループバック束縛のため、
実機検証にはHTTPS化と`0.0.0.0`束縛が必要。

- 検証時のLAN IP例: `192.168.1.105`(`hostname -I`で再確認)
- ポート例: `8443`
- アクセス例: `https://192.168.1.105:8443/html/add.html`

## 前提

- プロジェクトルート: `/home/tekkamelon/Documents/github/book_manager`
- 既存の`cgi_server.py`は変更しない。新規`https_cgi_server.py`で試す。
- CGI・binは変更しない。映像はサーバーに送らない。

## 例1: Python標準ライブラリのみでHTTPS化(自己署名)

追加依存なし。`cgi_server.py`をSSLで包む方法。

### 1-1. 証明書の作成

```sh
# プロジェクトルートで実行
mkdir -p certs
openssl req -x509 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -days 825 -nodes \
  -subj "/CN=192.168.1.105" \
  -addext "subjectAltName=IP:192.168.1.105,DNS:localhost,IP:127.0.0.1"
```

- `CN`と`subjectAltName`はiPhoneからアクセスするPCのLAN IPに合わせる
- IPが変わるたびに作り直しが必要
- `certs/`は公開リポジトリに含めない(`.gitignore`推奨)

### 1-2. `https_cgi_server.py`の例

```python
#!/usr/bin/env python3
# HTTPS version of cgi_server.py (local iPhone verification only)
import ssl
from http.server import CGIHTTPRequestHandler
from cgi_server import CGICompatHTTPServer, Handler

PORT = 8443
CERT_FILE = "certs/cert.pem"
KEY_FILE = "certs/key.pem"

# 127.0.0.1ではiPhoneから届かないため0.0.0.0で待つ
with CGICompatHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT_FILE, KEY_FILE)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"HTTPS CGI: https://192.168.1.105:{PORT}/html/add.html")
    httpd.serve_forever()
```

### 1-3. 起動とアクセス

```sh
python3 https_cgi_server.py
```

- iPhone Safariで`https://192.168.1.105:8443/html/add.html`を開く
- 自己署名のため初回は警告が出る。「詳細を表示」から「このWebサイトを閲覧」を選ぶ
- カメラ許可ダイアログが出れば成功

欠点: iOSのバージョンによっては警告突破だけでは`getUserMedia`が許可されない場合がある。その場合は例2が確実。

## 例2: `mkcert`で信頼済み証明書を作る(推奨)

iOSにルートCAをインストールするため、警告なしでHTTPSになる。実機検証が安定する。

```sh
# mkcertの導入(Ubuntuの例)
sudo apt install mkcert

# ローカルCAを作成
mkcert -install

# PCのLAN IPで証明書を作成
mkcert -cert-file certs/cert.pem -key-file certs/key.pem \
  192.168.1.105 localhost 127.0.0.1

# サーバーは例1と同じhttps_cgi_server.pyを使う
python3 https_cgi_server.py
```

iPhone側の手順:

1. `$(mkcert -CAROOT)/rootCA.pem`をiPhoneへ配布(AirDrop、メールなど)
2. iPhoneでプロファイルをインストール
3. 「設定」>「一般」>「情報」>「証明書信頼設定」でルートCAを「信頼」にする
4. `https://192.168.1.105:8443/html/add.html`を開く

## 例3: Caddyでリバースプロキシ(既存HTTPサーバーを触らない)

`cgi_server.py`はHTTPのまま、CaddyだけがHTTPS終端をする。

### Caddyfileの例

```text
https://192.168.1.105:8443 {
  tls certs/cert.pem certs/key.pem
  reverse_proxy 127.0.0.1:8000
}
```

### 起動例

```sh
# ターミナル1: 既存サーバー
python3 cgi_server.py

# ターミナル2: プロキシ
caddy run --config Caddyfile --adapter caddyfile
```

- `certs/`は例1または例2で作成したものを使う
- CGIの挙動を変えずにHTTPSだけ足せる

## 例4: 一時的なトンネル(開発時のみ)

LAN内mDNSや証明書配布が面倒な場合の一時策。

```sh
# cloudflaredの例(HTTPの8000番を公開URLでHTTPS化)
cloudflared tunnel --url http://localhost:8000
```

- 発行された`https://xxx.trycloudflare.com/html/add.html`をiPhoneで開く
- 正規の証明書なので警告が出ない
- URL自体は外部公開になるため、蔵書データのある検証では使わない

## おすすめ

- 自宅LANでの検証: 例2(`mkcert`)+例1の`https_cgi_server.py`が最良
- コードを汚さない別案: 例3(Caddy)
- ファイアウォールで`8443/tcp`の許可が必要な場合がある。開かない時は`sudo ufw allow 8443/tcp`を確認

## 注意事項

- `certs/*.pem`や`Caddyfile`のIP部分は環境依存のためcommitしない
- 本ファイルは手順例のみ。`https_cgi_server.py`本体の追加は別作業とする
- commitは指示があるまで行わない(本ファイルの追加commitは別途指示あり)
