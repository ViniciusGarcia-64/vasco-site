import requests
from bs4 import BeautifulSoup
from supabase import create_client

# 1. COLE SUAS CHAVES AQUI DENTRO DAS ASPAS:
SUPABASE_URL = "https://rzckltwastxfbwkgkndl.supabase.co"
SUPABASE_KEY = "sb_secret_OsvFvagriM7QYhTulrubag_7RXWiSWp"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def coletar_noticias():
    print("Buscando últimas notícias do Vasco...")
    url = "https://ge.globo.com/futebol/times/vasco/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    resposta = requests.get(url, headers=headers)
    if resposta.status_code != 200:
        print(f"Erro ao acessar site: {resposta.status_code}")
        return

    soup = BeautifulSoup(resposta.text, "html.parser")
    links = soup.select(".feed-post-link")

    for item in links[:5]:
        titulo = item.text.strip()
        link = item.get("href")

        if titulo and link:
            dados = {"titulo": titulo, "link": link, "fonte": "ge.globo"}
            try:
                supabase.table("noticias").upsert(dados, on_conflict="link").execute()
                print(f"Salvo: {titulo}")
            except Exception as e:
                print(f"Erro ao salvar: {e}")

if __name__ == "__main__":
    coletar_noticias()