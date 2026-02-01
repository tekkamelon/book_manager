#!/usr/bin/env python3
import socketserver


from http.server import CGIHTTPRequestHandler

# CGIディレクトリを指定 (デフォルト cgi-bin)
PORT = 8000
HandlerClass = CGIHTTPRequestHandler
HandlerClass.cgi_directories = ['/cgi-bin']


with socketserver.TCPServer(("127.0.0.1", PORT), HandlerClass) as httpd:
    print(f"CGIサーバー起動: http://localhost:{PORT}/html/index.html (Ctrl+C停止)")
    httpd.serve_forever()
