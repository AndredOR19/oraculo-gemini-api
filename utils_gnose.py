import os
import requests
from datetime import datetime

# Chaves do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def calcular_mapa_completo(nome, data_nasc, hora, local):
    """
    Calcula o mapa astrológico básico
    (Versão simplificada enquanto resolvemos pyswisseph)
    """
    try:
        # Parsear data e hora
        ano, mes, dia = map(int, data_nasc.split('-'))
        hora_int, minuto = map(int, hora.split(':'))
        
        # Por enquanto, retorna dados básicos
        # TODO: Integrar cálculo astrológico completo
        resultado = {
            "nome": nome,
            "data_nascimento": data_nasc,
            "hora": hora,
            "local": local,
            "status": "calculado_basico",
            "nota": "Cálculos completos em desenvolvimento"
        }
        
        return resultado
        
    except Exception as e:
        return {"erro": f"Erro ao calcular mapa: {str(e)}"}