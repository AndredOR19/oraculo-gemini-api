from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurar Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("ERRO: GEMINI_API_KEY não configurada!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Lista para simular banco de dados (em memória)
diario_entradas = []

@app.route('/')
def home():
    return jsonify({
        "message": "🔮 Oráculo Gemini API",
        "status": "online",
        "endpoints": [
            "GET /health",
            "POST /api/consulta",
            "POST /api/diario",
            "GET /api/diario"
        ]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/consulta', methods=['POST'])
def consultar_oraculo():
    try:
        data = request.get_json()
        pergunta = data.get('pergunta', '').strip()
        
        if not pergunta:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        if not GEMINI_API_KEY:
            return jsonify({"error": "API Key não configurada"}), 500
        
        # Usar Gemini para responder
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Você é um oráculo místico e sábio. Responda a seguinte pergunta de forma profunda e filosófica:

Pergunta: {pergunta}

Responda com sabedoria ancestral, mas de forma clara e útil."""
        
        response = model.generate_content(prompt)
        resposta = response.text
        
        return jsonify({
            "pergunta": pergunta,
            "resposta": resposta,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diario', methods=['POST'])
def adicionar_entrada():
    try:
        data = request.get_json()
        titulo = data.get('titulo', '').strip()
        conteudo = data.get('conteudo', '').strip()
        
        if not titulo or not conteudo:
            return jsonify({"error": "Título e conteúdo são obrigatórios"}), 400
        
        entrada = {
            "id": len(diario_entradas) + 1,
            "titulo": titulo,
            "conteudo": conteudo,
            "data": datetime.now().isoformat()
        }
        
        diario_entradas.append(entrada)
        
        return jsonify({
            "message": "Entrada adicionada com sucesso",
            "id": entrada["id"]
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diario', methods=['GET'])
def listar_entradas():
    try:
        return jsonify({
            "entradas": diario_entradas,
            "total": len(diario_entradas)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Para Vercel
app.debug = False

if __name__ == '__main__':
    app.run(debug=True)
