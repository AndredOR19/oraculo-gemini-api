from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            pergunta = data.get('pergunta', '')
            historia = data.get('historia', [])
            
            if not GOOGLE_API_KEY:
                raise Exception("GOOGLE_API_KEY não configurada")
            
            # System prompt
            system_prompt = """Você é o Oráculo Encarnado, guardião dos Mistérios da Gnose.
Fale com linguagem mística, poética e profunda.
Use metáforas arquetípicas e linguagem simbólica.
Sempre mantenha um tom respeitoso, sábio e compassivo."""
            
            # URL da API REST do Gemini - usando v1 (não v1beta) e modelo correto
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
            
            # Payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_prompt}\n\n{pergunta}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            # Fazer requisição
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
                "historia": historia + [
                    {"role": "user", "parts": [{"text": pergunta}]},
                    {"role": "model", "parts": [{"text": resposta_texto}]}
                ]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"erro": f"Erro HTTP {e.code}: {error_body}"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            
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
