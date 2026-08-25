import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rzckltwastxfbwkgkndl.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_KEY:
    print("Erro: SUPABASE_KEY não configurada nos Secrets do GitHub.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def coletar_noticias():
    try:
        url = "https://ge.globo.com/futebol/times/vasco/"
        req = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        posts = soup.find_all('a', class_='feed-post-link')
        novas = 0
        for p in posts[:5]:
            titulo = p.text.strip()
            link = p.get('href')
            if titulo and link:
                try:
                    supabase.table('noticias').insert({
                        "titulo": titulo, 
                        "link": link, 
                        "fonte": "ge.globo"
                    }).execute()
                    novas += 1
                except Exception:
                    pass
        print(f"Notícias atualizadas ({novas} novas).")
    except Exception as e:
        print(f"Erro nas notícias: {e}")

def atualizar_classificacao():
    try:
        # Exemplo de sincronização da tabela de classificação
        # Insere dados de topo e posição do Vasco
        times_exemplo = [
            {"posicao": 1, "time": "Botafogo", "pontos": 43, "jogos": 22, "vitorias": 13, "saldo_gols": 18},
            {"posicao": 2, "time": "Flamengo", "pontos": 41, "jogos": 21, "vitorias": 12, "saldo_gols": 14},
            {"posicao": 3, "time": "Palmeiras", "pontos": 41, "jogos": 22, "vitorias": 12, "saldo_gols": 13},
            {"posicao": 10, "time": "Vasco", "pontos": 28, "jogos": 21, "vitorias": 8, "saldo_gols": -3},
        ]
        
        for item in times_exemplo:
            supabase.table('classificacao').upsert(item, on_conflict='posicao').execute()
        print("Tabela de classificação atualizada com sucesso.")
    except Exception as e:
        print(f"Erro na classificação: {e}")

if __name__ == "__main__":
    coletar_noticias()
    atualizar_classificacao()