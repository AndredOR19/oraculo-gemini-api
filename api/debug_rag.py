from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            debug_info = {
                "env_vars": {
                    "SUPABASE_URL": os.environ.get("SUPABASE_URL", "NOT SET")[:50] + "...",
                    "SUPABASE_SERVICE_ROLE_KEY": bool(os.environ.get("SUPABASE_SERVICE_ROLE_KEY")),
                    "GOOGLE_API_KEY": bool(os.environ.get("GOOGLE_API_KEY"))
                },
                "pasta_rag_existe": os.path.exists("/var/task/api/rag"),
                "arquivos_rag": [],
                "testes": {}
            }
            
            # Listar arquivos na pasta rag
            try:
                import glob
                debug_info["arquivos_rag"] = glob.glob("/var/task/api/rag/*")
            except Exception as e:
                debug_info["erro_listar_rag"] = str(e)
            
            # Teste 1: Import
            try:
                from rag import montar_contexto
                debug_info["testes"]["import_rag"] = "✅ SUCCESS"
            except Exception as e:
                debug_info["testes"]["import_rag"] = f"❌ ERRO: {str(e)}"
            
            # Teste 2: Buscar letra "Aleph"
            try:
                from rag.supabase_search import buscar_letra
                resultado = buscar_letra("Aleph")
                debug_info["testes"]["buscar_aleph"] = {
                    "status": "✅ SUCCESS" if resultado else "⚠️ Sem resultados",
                    "quantidade": len(resultado),
                    "dados": resultado[:1] if resultado else None
                }
            except Exception as e:
                debug_info["testes"]["buscar_aleph"] = f"❌ ERRO: {str(e)}"
            
            # Teste 3: Buscar arquétipo "Touro"
            try:
                from rag.supabase_search import buscar_arquetipo
                resultado = buscar_arquetipo("Touro")
                debug_info["testes"]["buscar_touro"] = {
                    "status": "✅ SUCCESS" if resultado else "⚠️ Sem resultados",
                    "quantidade": len(resultado),
                    "dados": resultado[:1] if resultado else None
                }
            except Exception as e:
                debug_info["testes"]["buscar_touro"] = f"❌ ERRO: {str(e)}"
            
            # Teste 4: Montar contexto completo
            try:
                from rag import montar_contexto
                contexto = montar_contexto("O que significa a letra Aleph?")
                debug_info["testes"]["montar_contexto"] = {
                    "status": "✅ SUCCESS" if contexto else "⚠️ Contexto vazio",
                    "tamanho": len(contexto) if contexto else 0,
                    "preview": contexto[:200] if contexto else None
                }
            except Exception as e:
                debug_info["testes"]["montar_contexto"] = f"❌ ERRO: {str(e)}\n{traceback.format_exc()}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(debug_info, indent=2, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            error_response = {"erro": str(e), "traceback": traceback.format_exc()}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
