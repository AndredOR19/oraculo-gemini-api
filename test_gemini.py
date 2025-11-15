import google.generativeai as genai
import os

# Substitua pela sua chave real
GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)

# Listar modelos disponíveis
print("Modelos disponíveis:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")

# Testar geração
print("\nTestando gemini-pro:")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Diga olá em uma frase")
print(f"Resposta: {response.text}")
