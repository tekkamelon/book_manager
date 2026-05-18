#!/usr/bin/env python3
from http.server import HTTPServer, CGIHTTPRequestHandler

# CGIディレクトリを指定 (デフォルト cgi-bin)
PORT = 8000


class CGICompatHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_name = "localhost"


class Handler(CGIHTTPRequestHandler):
    cgi_directories = ['/cgi-bin']


with CGICompatHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"CGIサーバー起動: http://localhost:{PORT}/html/index.html (Ctrl+C停止)")
    httpd.serve_forever()
