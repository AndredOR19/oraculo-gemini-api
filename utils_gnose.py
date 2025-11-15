import os
import requests
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Chaves do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def calcular_mapa_completo(nome, data_nasc, hora, local):
    """
    Calcula o mapa astrológico completo
    
    Args:
        nome: Nome da pessoa
        data_nasc: Data no formato "YYYY-MM-DD"
        hora: Hora no formato "HH:MM"
        local: Local de nascimento (ex: "Vacaria, RS")
    
    Returns:
        dict com os dados do mapa calculado
    """
    try:
        # Parsear data e hora
        ano, mes, dia = map(int, data_nasc.split('-'))
        hora_int, minuto = map(int, hora.split(':'))
        
        # Por enquanto, coordenadas fixas (você pode integrar geocoding depois)
        # Exemplo: Vacaria, RS
        lat = -28.5
        lon = -50.8
        
        # Criar objetos Flatlib
        dt = Datetime(f'{ano}/{mes}/{dia}', f'{hora_int}:{minuto}', '+00:00')
        pos = GeoPos(lat, lon)
        
        # Calcular o mapa
        chart = Chart(dt, pos)
        
        # Extrair dados básicos
        sol = chart.get('Sun')
        lua = chart.get('Moon')
        asc = chart.get('Asc')
        
        resultado = {
            "nome": nome,
            "data_nascimento": data_nasc,
            "hora": hora,
            "local": local,
            "sol": {
                "signo": sol.sign,
                "grau": float(sol.signlon)
            },
            "lua": {
                "signo": lua.sign,
                "grau": float(lua.signlon)
            },
            "ascendente": {
                "signo": asc.sign,
                "grau": float(asc.signlon)
            }
        }
        
        return resultado
        
    except Exception as e:
        return {"erro": f"Erro ao calcular mapa: {str(e)}"}
