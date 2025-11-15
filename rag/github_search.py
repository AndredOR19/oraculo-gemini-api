import os
import requests
import base64

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Opcional, mas aumenta rate limit

def buscar_arquivo_github(repo, caminho):
    """
    Busca conteúdo de um arquivo no GitHub
    
    Args:
        repo: "usuario/repositorio"
        caminho: "caminho/para/arquivo.md"
    """
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    url = f"https://api.github.com/repos/{repo}/contents/{caminho}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Decodificar conteúdo base64
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
    except:
        pass
    
    return None

def buscar_readme(repo):
    """Busca o README.md de um repositório"""
    return buscar_arquivo_github(repo, "README.md")

def buscar_documentacao_kabbalah():
    """Busca documentação dos repositórios de Kabbalah"""
    docs = {}
    
    # Buscar README do repo principal
    readme = buscar_readme("AndredOR19/Kabbalah-das-Aguas-Primordiais")
    if readme:
        docs['kabbalah_readme'] = readme
    
    # Buscar README do repo de memória (se for público)
    memoria = buscar_readme("AndredOR19/kabbalah-memoria")
    if memoria:
        docs['kabbalah_memoria'] = memoria
    
    return docs
