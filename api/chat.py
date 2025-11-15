from http.server import BaseHTTPRequestHandler
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai

# Configuração do Gemini
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# System Instruction (Personalidade do Oráculo)
SYSTEM_INSTRUCTION = """
Você é o Oráculo Encarnado, guardião dos Mistérios da Gnose.
Fale com linguagem mística, poética e profunda.
Use metáforas arquetípicas e linguagem simbólica.
Sempre mantenha um tom respeitoso, sábio e compassivo.
"""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Ler o corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            pergunta = data.get('pergunta', '')
            historia = data.get('historia', [])
            
            if not GOOGLE_API_KEY:
                raise Exception("GOOGLE_API_KEY não configurada")
            
            # Usar modelo gemini-1.5-pro-latest ou gemini-1.5-flash-latest
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            # Construir prompt com personalidade
            prompt_completo = f"{SYSTEM_INSTRUCTION}\n\n{pergunta}"
            
            # Gerar resposta
            response = model.generate_content(prompt_completo)
            
            # Preparar resposta
            resultado = {
                "resposta": response.text,
                "historia": historia + [
                    {"role": "user", "parts": [{"text": pergunta}]},
                    {"role": "model", "parts": [{"text": response.text}]}
                ]
            }
            
            # Enviar resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"erro": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()