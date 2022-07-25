from http.server import HTTPServer, CGIHTTPRequestHandler
#создаем локальный сервер с портом http://localhost:8000
server_address = ("", 8000)
#создаем сервер
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
#запускаем, чтобы работал пока не надоест или пока не остановим
#команда для терминала
#python3 -m http.server --cgi

#http://localhost:63342/project_qr/index.html

httpd.serve_forever()