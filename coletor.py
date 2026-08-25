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
                    # Ignora se a notícia já estiver cadastrada
                    pass
        print(f"Coleta finalizada! {novas} novas notícias inseridas.")
    except Exception as e:
        print(f"Erro ao acessar ge.globo: {e}")

if __name__ == "__main__":
    coletar_noticias()