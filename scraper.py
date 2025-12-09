import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def scrape_category(base_url, pages):
    data = []
    print(f"Scraping {pages} pages from {base_url}...")

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        try:
            response = session.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print(f"Erreur page {page}: {e}")
            continue

        soup = bs(response.content, "html.parser")
        cards = soup.find_all('div', class_='ad__card')

        if not cards:
            print(f"Plus de produits à la page {page}")
            break

        for item in cards:
            try:
                title_tag = item.find('p', class_='ad__card-description')
                type_name = title_tag.get_text(strip=True) if title_tag else "No name"

                price_tag = item.find('p', class_='ad__card-price')
                price = price_tag.get_text(strip=True) if price_tag else "0 CFA"

                location_tag = item.find('p', class_='ad__card-location')
                address = "Dakar"
                if location_tag:
                    span = location_tag.find('span')
                    if span:
                        address = span.get_text(strip=True)

                img_tag = item.find('img')
                image_link = img_tag['src'] if img_tag and img_tag.get('src') else ""

                data.append({
                    'type': type_name,
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except Exception:
                continue

        time.sleep(1) 

    # Nettoyage des données
    df = pd.DataFrame(data)
    if not df.empty:
        df['price'] = df['price'].str.replace('CFA', '', regex=True)
        df['price'] = df['price'].str.replace(r'\D', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        mean_price = df['price'].mean()
        df['price'] = df['price'].fillna(mean_price).astype(int)
        df = df.drop_duplicates().reset_index(drop=True)

    return df



def scrape_clothes_men(pages):
    return scrape_category("https://sn.coinafrique.com/categorie/vetements-homme", pages)


def scrape_clothes_kids(pages):
    return scrape_category("https://sn.coinafrique.com/categorie/vetements-enfants", pages)


def scrape_shoes_men(pages):
    return scrape_category("https://sn.coinafrique.com/categorie/chaussures-homme", pages)


def scrape_shoes_kids(pages):
    return scrape_category("https://sn.coinafrique.com/categorie/chaussures-enfants", pages)
