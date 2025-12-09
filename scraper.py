from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd


def scrape_clothes_men(pages):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = []
    
    for p in range(1, pages + 1):
        driver.get(f"https://sn.coinafrique.com/categorie/vetements-homme?page={p}")
        soup = bs(driver.page_source, 'html.parser')
        for item in soup.find_all('div', class_='ad__card'):
            try:
                
                title = item.find('p', class_='ad__card-description')
                type_name = title.get_text(strip=True) if title else "No name"
                
                price = item.find('p', class_='ad__card-price').text.strip()
                address = item.find('p', class_='ad__card-location').find('span').text.strip() if item.find('p', class_='ad__card-location') else "Dakar"
                image_link = item.find('img')['src']
                
                data.append({
                    'type': type_name,      
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except:
                pass
    
    driver.quit()
    
    df = pd.DataFrame(data)
    df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    mean_price = df['price'].mean()
    df['price'] = df['price'].fillna(mean_price).astype(int)
    df.drop_duplicates(inplace=True)
    
    return df


def scrape_clothes_kids(pages):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = []
    
    for p in range(1, pages + 1):
        driver.get(f"https://sn.coinafrique.com/categorie/vetements-enfants?page={p}")
        soup = bs(driver.page_source, 'html.parser')
        for item in soup.find_all('div', class_='ad__card'):
            try:
                title = item.find('p', class_='ad__card-description')
                type_name = title.get_text(strip=True) if title else "No name"
                
                price = item.find('p', class_='ad__card-price').text.strip()
                address = item.find('p', class_='ad__card-location').find('span').text.strip() if item.find('p', class_='ad__card-location') else "Dakar"
                image_link = item.find('img')['src']
                
                data.append({
                    'type': type_name,
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except:
                pass
    
    driver.quit()
    
    df = pd.DataFrame(data)
    df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    mean_price = df['price'].mean()
    df['price'] = df['price'].fillna(mean_price).astype(int)
    df.drop_duplicates(inplace=True)
    
    return df


def scrape_shoes_men(pages):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = []
    
    for p in range(1, pages + 1):
        driver.get(f"https://sn.coinafrique.com/categorie/chaussures-homme?page={p}")
        soup = bs(driver.page_source, 'html.parser')
        for item in soup.find_all('div', class_='ad__card'):
            try:
                title = item.find('p', class_='ad__card-description')
                type_name = title.get_text(strip=True) if title else "No name"
                
                price = item.find('p', class_='ad__card-price').text.strip()
                address = item.find('p', class_='ad__card-location').find('span').text.strip() if item.find('p', class_='ad__card-location') else "Dakar"
                image_link = item.find('img')['src']
                
                data.append({
                    'type': type_name,
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except:
                pass
    
    driver.quit()
    
    df = pd.DataFrame(data)
    df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    mean_price = df['price'].mean()
    df['price'] = df['price'].fillna(mean_price).astype(int)
    df.drop_duplicates(inplace=True)
    
    return df


def scrape_shoes_kids(pages):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = []
    
    for p in range(1, pages + 1):
        driver.get(f"https://sn.coinafrique.com/categorie/chaussures-enfants?page={p}")
        soup = bs(driver.page_source, 'html.parser')
        for item in soup.find_all('div', class_='ad__card'):
            try:
                title = item.find('p', class_='ad__card-description')
                type_name = title.get_text(strip=True) if title else "No name"
                
                price = item.find('p', class_='ad__card-price').text.strip()
                address = item.find('p', class_='ad__card-location').find('span').text.strip() if item.find('p', class_='ad__card-location') else "Dakar"
                image_link = item.find('img')['src']
                
                data.append({
                    'type': type_name,
                    'price': price,
                    'address': address,
                    'image_link': image_link
                })
            except:
                pass
    
    driver.quit()
    
    df = pd.DataFrame(data)
    df['price'] = df['price'].str.replace('CFA', '').str.replace(r'\D', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    mean_price = df['price'].mean()
    df['price'] = df['price'].fillna(mean_price).astype(int)
    df.drop_duplicates(inplace=True)
    
    return df