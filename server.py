from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from log2json import action

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Здесь запускается ваш Python-код
        action()
        
        # Ответ на запрос
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'Python script executed successfully'}
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Сервер запущен на порту 8000...')
    httpd.serve_forever()
