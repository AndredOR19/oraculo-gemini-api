from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import urllib.request
import urllib.error

# Adicionar pasta pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag import montar_contexto

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            pergunta = data.get('pergunta', '')
            historia = data.get('historia', [])
            usar_rag = data.get('usar_rag', True)
            
            if not GOOGLE_API_KEY:
                raise Exception("GOOGLE_API_KEY não configurada")
            
            system_prompt = """Você é o Oráculo Encarnado, guardião dos Mistérios da Kabbalah das Águas Primordiais.
Fale com linguagem mística, poética e profunda.
Use metáforas arquetípicas e linguagem simbólica.
Sempre mantenha um tom respeitoso, sábio e compassivo."""
            
            # BUSCAR CONTEXTO (RAG)
            contexto_rag = ""
            if usar_rag:
                try:
                    contexto = montar_contexto(pergunta)
                    if contexto:
                        contexto_rag = f"\n\n### CONHECIMENTO SAGRADO DO SUPABASE:\n{contexto}\n"
                except Exception as e:
                    # Log do erro mas continua sem RAG
                    contexto_rag = f"\n\n[DEBUG: Erro ao buscar contexto: {str(e)}]\n"
            
            # Montar prompt completo
            prompt_completo = f"{system_prompt}{contexto_rag}\n\n### PERGUNTA DO BUSCADOR:\n{pergunta}"
            
            # Chamar Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt_completo}]
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            resposta_texto = result['candidates'][0]['content']['parts'][0]['text']
            
            resultado = {
                "resposta": resposta_texto,
                "contexto_usado": bool(contexto_rag and '[DEBUG' not in contexto_rag),
                "debug_contexto": contexto_rag if '[DEBUG' in contexto_rag else None,
                "historia": historia + [
                    {"role": "user", "parts": [{"text": pergunta}]},
                    {"role": "model", "parts": [{"text": resposta_texto}]}
                ]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            error_response = {"erro": str(e), "tipo": type(e).__name__}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
