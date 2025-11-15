from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import traceback

# Adicionar pasta atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            debug_info = {
                "sys_path": sys.path[:5],
                "current_dir": os.path.dirname(os.path.abspath(__file__)),
                "env_vars": {
                    "SUPABASE_URL": bool(os.environ.get("SUPABASE_URL")),
                    "SUPABASE_KEY": bool(os.environ.get("SUPABASE_SERVICE_ROLE_KEY")),
                    "GOOGLE_API_KEY": bool(os.environ.get("GOOGLE_API_KEY"))
                },
                "arquivos_api": [],
                "import_test": {}
            }
            
            # Listar arquivos na pasta api
            try:
                import glob
                debug_info["arquivos_api"] = glob.glob("/var/task/api/*")
            except Exception as e:
                debug_info["erro_listar"] = str(e)
            
            # Testar import do rag
            try:
                from rag import montar_contexto
                debug_info["import_test"]["rag"] = "SUCCESS"
                debug_info["import_test"]["montar_contexto"] = str(type(montar_contexto))
            except Exception as e:
                debug_info["import_test"]["rag"] = f"ERRO: {str(e)}"
                debug_info["import_test"]["traceback"] = traceback.format_exc()
            
            # Testar busca no Supabase
            try:
                from rag.supabase_search import buscar_letra
                resultado = buscar_letra("aleph")
                debug_info["import_test"]["supabase_search"] = f"SUCCESS - Encontrou {len(resultado)} resultados"
            except Exception as e:
                debug_info["import_test"]["supabase_search"] = f"ERRO: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(debug_info, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"erro": str(e), "traceback": traceback.format_exc()}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
