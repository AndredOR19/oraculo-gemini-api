from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Adiciona o diretório raiz ao path para importar utils_gnose
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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
            
            # Configurar o modelo Gemini
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=SYSTEM_INSTRUCTION,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            # Iniciar chat com histórico
            chat = model.start_chat(history=historia)
            
            # Enviar mensagem
            response = chat.send_message(pergunta)
            
            # Preparar resposta
            resultado = {
                "resposta": response.text,
                "historia": [
                    {"role": msg.role, "parts": [{"text": part.text} for part in msg.parts]}
                    for msg in chat.history
                ]
            }
            
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
