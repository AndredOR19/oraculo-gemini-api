from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils_gnose import calcular_mapa_completo

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Ler dados da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            nome = data.get('nome')
            data_nasc = data.get('data')
            hora = data.get('hora')
            local = data.get('local')
            
            # Validar dados
            if not all([nome, data_nasc, hora, local]):
                raise ValueError("Dados incompletos: nome, data, hora e local são obrigatórios")
            
            # Calcular mapa
            resultado = calcular_mapa_completo(nome, data_nasc, hora, local)
            
            # Enviar resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"erro": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
