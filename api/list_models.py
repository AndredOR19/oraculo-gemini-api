from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if not GOOGLE_API_KEY:
                raise Exception("GOOGLE_API_KEY não configurada")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            models_with_generate = []
            for model in result.get('models', []):
                methods = model.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    models_with_generate.append(model.get('name'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'models': models_with_generate
            }, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"erro": str(e)}).encode('utf-8'))
