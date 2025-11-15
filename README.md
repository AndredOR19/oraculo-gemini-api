# Oráculo Gemini API

API com Google Gemini AI para consultas místicas e cálculos astrológicos SCII.

## Endpoints

- `GET /api/health` - Health check
- `POST /api/chat` - Conversa com o Oráculo (Gemini AI)
- `POST /api/calcular_mapa` - Cálculo de mapa astrológico

## Deploy no Vercel

1. Conecte este repositório ao Vercel
2. Configure as Environment Variables:
   - `GOOGLE_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`

## Desenvolvimento Local
```bash
pip install -r requirements.txt
vercel dev
```
