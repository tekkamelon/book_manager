#!/usr/bin/env python3
import http.server
import socketserver
import os
from http.server import CGIHTTPRequestHandler

# CGIディレクトリを指定 (デフォルト cgi-bin)
PORT = 8000
HandlerClass = CGIHTTPRequestHandler
HandlerClass.cgi_directories = ['/cgi-bin']
with socketserver.TCPServer(("127.0.0.1", PORT), HandlerClass) as httpd:
    print("CGIサーバー起動: http://localhost:{}/html/index.html (Ctrl+C停止)".format(PORT))
    httpd.serve_forever()