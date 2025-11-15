from .supabase_search import buscar_contexto_completo
from .github_search import buscar_documentacao_kabbalah
import re

def extrair_termos_chave(pergunta):
    """
    Extrai termos-chave da pergunta
    
    Identifica: letras hebraicas, planetas, signos, etc.
    """
    # Lista de termos conhecidos
    letras = ['aleph', 'beth', 'gimel', 'daleth', 'he', 'vav', 'zayin', 'cheth', 
              'teth', 'yod', 'kaph', 'lamed', 'mem', 'nun', 'samekh']
    
    planetas = ['sol', 'lua', 'mercúrio', 'mercurio', 'vênus', 'venus', 
                'marte', 'júpiter', 'jupiter', 'saturno', 'urano', 'netuno', 'plutão', 'plutao']
    
    signos = ['áries', 'aries', 'touro', 'gêmeos', 'gemeos', 'câncer', 'cancer',
              'leão', 'leao', 'virgem', 'libra', 'escorpião', 'escorpiao', 
              'sagitário', 'sagitario', 'capricórnio', 'capricornio', 'aquário', 'aquario', 'peixes']
    
    pergunta_lower = pergunta.lower()
    termos_encontrados = []
    
    # Buscar letras
    for letra in letras:
        if letra in pergunta_lower:
            termos_encontrados.append(letra)
    
    # Buscar planetas
    for planeta in planetas:
        if planeta in pergunta_lower:
            termos_encontrados.append(planeta)
    
    # Buscar signos
    for signo in signos:
        if signo in pergunta_lower:
            termos_encontrados.append(signo)
    
    return termos_encontrados

def montar_contexto(pergunta):
    """
    Monta contexto completo para o Gemini
    
    Returns:
        String formatada com todo o contexto relevante
    """
    # Extrair termos
    termos = extrair_termos_chave(pergunta)
    
    contexto_texto = ""
    
    if termos:
        # Buscar no Supabase
        dados_supabase = buscar_contexto_completo(termos)
        
        if dados_supabase['letras']:
            contexto_texto += "\n### LETRAS HEBRAICAS:\n"
            for letra in dados_supabase['letras']:
                contexto_texto += f"- {letra.get('nome_letra')}: {letra.get('pictografia', '')}\n"
        
        if dados_supabase['arquetipos']:
            contexto_texto += "\n### ARQUETIPOS:\n"
            for arq in dados_supabase['arquetipos']:
                tipo = arq.get('tipo_arquetipo', '')
                nome = arq.get('nome_arquetipo', '')
                contexto_texto += f"- {nome} ({tipo})\n"
    
    # Buscar documentação (opcional, pode ser lento)
    # docs = buscar_documentacao_kabbalah()
    # if docs:
    #     contexto_texto += "\n### DOCUMENTAÇÃO:\n"
    #     contexto_texto += docs.get('kabbalah_readme', '')[:500]  # Primeiros 500 chars
    
    return contexto_texto if contexto_texto else None
