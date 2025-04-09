import http.server
import socketserver
import json
from urllib.parse import urlparse

PORT = 5500

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"message": "Servidor funcionando!"}
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"Requisição recebida: {args[0]} {args[1]} {args[2]}")

print(f"Iniciando servidor em http://localhost:{PORT}")
print("Tente acessar essa URL no seu navegador")
print("Pressione Ctrl+C para parar o servidor")

# Cria o servidor
with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever() 