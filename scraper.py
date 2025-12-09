from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def _get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService,OptimizeWebFonts")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_clothes_men(pages):
    driver = _get_driver()
    data = []
    try:
        for p in range(1, pages + 1):
            url = f"https://sn.coinafrique.com/categorie/vetements-homme?page={p}"
            driver.get(url)
            time.sleep(3)  # petit délai pour charger
            soup = bs(driver.page_source, 'html.parser')
            for item in soup.find_all('div', class_='ad__card'):
                try:
                    title = item.find('p', class_='ad__card-description')
                    type_name = title.get_text(strip=True) if title else "No name"
                    price = item.find('p', class_='ad__card-price')
                    price = price.get_text(strip=True) if price else "0 CFA"
                    address = item.find('p', class_='ad__card-location')
                    address = address.find('span').get_text(strip=True) if address and address.find('span') else "Dakar"
                    img = item.find('img')
                    image_link = img['src'] if img and 'src' in img.attrs else ""
                    data.append({'type': type_name, 'price': price, 'address': address, 'image_link': image_link})
                except:
                    continue
    finally:
        driver.quit()

    df = pd.DataFrame(data)
    if not df.empty:
        df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(df['price'].mean()).astype(int)
        df.drop_duplicates(inplace=True)
    return df

# 
def scrape_clothes_kids(pages):
    driver = _get_driver()
    data = []
    try:
        for p in range(1, pages + 1):
            driver.get(f"https://sn.coinafrique.com/categorie/vetements-enfants?page={p}")
            time.sleep(3)
            soup = bs(driver.page_source, 'html.parser')
            for item in soup.find_all('div', class_='ad__card'):
                try:
                    title = item.find('p', class_='ad__card-description')
                    type_name = title.get_text(strip=True) if title else "No name"
                    price = item.find('p', class_='ad__card-price')
                    price = price.get_text(strip=True) if price else "0 CFA"
                    address = item.find('p', class_='ad__card-location')
                    address = address.find('span').get_text(strip=True) if address and address.find('span') else "Dakar"
                    img = item.find('img')
                    image_link = img['src'] if img and 'src' in img.attrs else ""
                    data.append({'type': type_name, 'price': price, 'address': address, 'image_link': image_link})
                except:
                    continue
    finally:
        driver.quit()
    df = pd.DataFrame(data)
    if not df.empty:
        df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(df['price'].mean()).astype(int)
        df.drop_duplicates(inplace=True)
    return df

def scrape_shoes_men(pages):
    driver = _get_driver()
    data = []
    try:
        for p in range(1, pages + 1):
            driver.get(f"https://sn.coinafrique.com/categorie/chaussures-homme?page={p}")
            time.sleep(3)
            soup = bs(driver.page_source, 'html.parser')
            for item in soup.find_all('div', class_='ad__card'):
                try:
                    title = item.find('p', class_='ad__card-description')
                    type_name = title.get_text(strip=True) if title else "No name"
                    price = item.find('p', class_='ad__card-price')
                    price = price.get_text(strip=True) if price else "0 CFA"
                    address = item.find('p', class_='ad__card-location')
                    address = address.find('span').get_text(strip=True) if address and address.find('span') else "Dakar"
                    img = item.find('img')
                    image_link = img['src'] if img and 'src' in img.attrs else ""
                    data.append({'type': type_name, 'price': price, 'address': address, 'image_link': image_link})
                except:
                    continue
    finally:
        driver.quit()
    df = pd.DataFrame(data)
    if not df.empty:
        df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(df['price'].mean()).astype(int)
        df.drop_duplicates(inplace=True)
    return df

def scrape_shoes_kids(pages):
    driver = _get_driver()
    data = []
    try:
        for p in range(1, pages + 1):
            driver.get(f"https://sn.coinafrique.com/categorie/chaussures-enfants?page={p}")
            time.sleep(3)
            soup = bs(driver.page_source, 'html.parser')
            for item in soup.find_all('div', class_='ad__card'):
                try:
                    title = item.find('p', class_='ad__card-description')
                    type_name = title.get_text(strip=True) if title else "No name"
                    price = item.find('p', class_='ad__card-price')
                    price = price.get_text(strip=True) if price else "0 CFA"
                    address = item.find('p', class_='ad__card-location')
                    address = address.find('span').get_text(strip=True) if address and address.find('span') else "Dakar"
                    img = item.find('img')
                    image_link = img['src'] if img and 'src' in img.attrs else ""
                    data.append({'type': type_name, 'price': price, 'address': address, 'image_link': image_link})
                except:
                    continue
    finally:
        driver.quit()
    df = pd.DataFrame(data)
    if not df.empty:
        df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(df['price'].mean()).astype(int)
        df.drop_duplicates(inplace=True)
    return df
