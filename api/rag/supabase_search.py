import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
# Aceitar ambos os nomes
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")

def buscar_letra(nome_letra):
    """Busca informações sobre uma letra hebraica"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    # Buscar letra com case-insensitive e wildcard
    url = f"{SUPABASE_URL}/rest/v1/letras?nome_letra=ilike.{nome_letra}*&select=*"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar letra: {e}")
    
    return []

def buscar_arquetipo(nome_arquetipo):
    """Busca informações sobre um arquétipo (planeta/signo)"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    url = f"{SUPABASE_URL}/rest/v1/arquetipos?nome_arquetipo=ilike.{nome_arquetipo}*&select=*"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar arquétipo: {e}")
    
    return []

def buscar_correspondencias(letra_id=None, arquetipo_id=None):
    """Busca correspondências entre letras e arquetipos"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    if letra_id:
        url = f"{SUPABASE_URL}/rest/v1/scii_correspondencias?letra_id=eq.{letra_id}&select=*"
    elif arquetipo_id:
        url = f"{SUPABASE_URL}/rest/v1/scii_correspondencias?arquetipo_id=eq.{arquetipo_id}&select=*"
    else:
        return []
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar correspondências: {e}")
    
    return []

def buscar_contexto_completo(termos):
    """
    Busca contexto completo baseado em termos da pergunta
    
    Args:
        termos: Lista de palavras-chave ["aleph", "touro", etc.]
    
    Returns:
        Dict com informações encontradas
    """
    contexto = {
        "letras": [],
        "arquetipos": [],
        "correspondencias": []
    }
    
    for termo in termos:
        # Buscar letras
        letras = buscar_letra(termo)
        if letras:
            contexto["letras"].extend(letras)
            
        # Buscar arquetipos
        arquetipos = buscar_arquetipo(termo)
        if arquetipos:
            contexto["arquetipos"].extend(arquetipos)
    
    return contexto
