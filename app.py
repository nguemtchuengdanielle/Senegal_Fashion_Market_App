
import streamlit as st
import pandas as pd
import base64
import os
import plotly.express as px
from scraper import (
    scrape_clothes_men,
    scrape_clothes_kids,
    scrape_shoes_men,
    scrape_shoes_kids
)


def add_bg():
    try:
        with open("background.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{background-image:url('data:image/jpeg;base64,{data}');background-size:cover;background-attachment:fixed;}}
        .title {{color:white;text-align:center;font-size:70px;text-shadow:4px 4px 15px black;}}
        .subtitle {{color:#ffd700;text-align:center;font-size:30px;}}
        .card {{background:rgba(255,255,255,0.96);padding:35px;border-radius:25px;margin:30px 0;box-shadow:0 15px 40px rgba(0,0,0,0.5);}}
        </style>
        """, unsafe_allow_html=True)
    except: pass
add_bg()
st.markdown("""
<h1 style="
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #ff9ff3, #54a0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 3px 3px 15px rgba(0,0,0,0.6);
    margin: 40px 0;
">
    COINAFRIQUE DATA APP
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style="
    text-align: center;
    color: #ffd700;
    font-size: 28px;
    margin-top: -20px;
    text-shadow: 2px 2px 8px black;
">
    Senegal Fashion Market •  2025
</h2>
""", unsafe_allow_html=True)

st.sidebar.image("logo.png", caption="CoinAfrique", width=145)
pages = st.sidebar.selectbox("Choose number of pages to scrape", options=list(range(1, 21)), index=4)
choice = st.sidebar.selectbox("Options", [
    'Scrape data using BeautifulSoup',
    'Download scraped data',
    'Dashboard of the data',
    'Evaluate the App'
], index=0)

#SESSION STATE POUR GARDER LES DONNÉES SCRAPÉES
if 'df_men_clothes' not in st.session_state:
    st.session_state.df_men_clothes = None
if 'df_kids_clothes' not in st.session_state:
    st.session_state.df_kids_clothes = None
if 'df_men_shoes' not in st.session_state:
    st.session_state.df_men_shoes = None
if 'df_kids_shoes' not in st.session_state:
    st.session_state.df_kids_shoes = None

# FONCTION D'AFFICHAGE DES DONNÉES
def show_data(df, title):
    st.markdown(f"<h2 style='text-align:center;color:#ff6b6b;text-shadow:2px 2px 8px black;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:white;font-size:18px;text-shadow:2px 2px 6px black;'><strong>{len(df):,} products</strong> | Dimension: {df.shape[0]} × {df.shape[1]}</p>", unsafe_allow_html=True)
    st.dataframe(df[['type', 'price', 'address','image_link']].head(20), use_container_width=True)
    st.download_button("DOWNLOAD FULL CSV", df.to_csv(index=False).encode(), f"{title}.csv", use_container_width=True)

#  SCRAPING le  MENU
if choice == 'Scrape data using BeautifulSoup':
    st.markdown("### Choose a category to scrape:")
    
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("Men's Clothes", use_container_width=True):
            with st.spinner("Scraping Men's Clothes..."):
                st.session_state.df_men_clothes = scrape_clothes_men(pages)
            show_data(st.session_state.df_men_clothes, "Men's Clothes")
            
        if st.button("Kids Clothes", use_container_width=True):
            with st.spinner("Scraping Kids Clothes..."):
                st.session_state.df_kids_clothes = scrape_clothes_kids(pages)
            show_data(st.session_state.df_kids_clothes, "Kids Clothes")
    
    with c2:
        if st.button("Men's Shoes", use_container_width=True):
            with st.spinner("Scraping Men's Shoes..."):
                st.session_state.df_men_shoes = scrape_shoes_men(pages)
            show_data(st.session_state.df_men_shoes, "Men's Shoes")
            
        if st.button("Kids Shoes", use_container_width=True):
            with st.spinner("Scraping Kids Shoes..."):
                st.session_state.df_kids_shoes = scrape_shoes_kids(pages)
            show_data(st.session_state.df_kids_shoes, "Kids Shoes")

# DOWNLOAD  DATA 

elif choice == 'Download scraped data':
    st.markdown("<h2 style='text-align:center;color:#ffd700;'>Download Data</h2>", unsafe_allow_html=True)

    folder = "uncleaned_data"
    if not os.path.exists(folder):
        st.error("Folder 'uncleaned_data' not found!")
        st.stop()

    files = {
        "Men's Clothes": "vetements-homme-coinafrique.csv",
        "Kids Clothes": "vetements-enfants-coinafrique.csv",
        "Men's Shoes": "chaussures-homme-coinafrique.csv",
        "Kids Shoes": "chaussures-enfants-coinafrique.csv"
    }

    col1, col2 = st.columns(2)

    for title, filename in files.items():
        with col1 if "Clothes" in title else col2:
            if st.button(title, use_container_width=True):
                path = os.path.join(folder, filename)
                
            
                data = []
                with open(path, 'r', encoding='cp1252') as f:
                    lines = f.readlines()
                    
                    for i, line in enumerate(lines):
                        if i == 0:  
                            continue
                        
                        # Enleve les guillemets extérieurs
                        line = line.strip().strip('"')
                        line = line.replace('""', '"')
                        
                        
                        parts = []
                        current = ""
                        in_quotes = False
                        
                        for char in line:
                            if char == '"':
                                in_quotes = not in_quotes
                            elif char == ',' and not in_quotes:
                                parts.append(current.strip().strip('"'))
                                current = ""
                                continue
                            current += char
                        
                        parts.append(current.strip().strip('"'))
                        
                        if len(parts) >= 6:
                            data.append(parts[:6])
                
                df = pd.DataFrame(data, columns=['web_scraper_order', 'web_scraper_start_url', 'type', 'price', 'address', 'image_link'])
                
                st.success(f" {filename} loaded")
                st.write(f"**{df.shape[0]} rows × {df.shape[1]} columns**")
                st.dataframe(df.head(20), use_container_width=True)
                
                st.download_button(" DOWNLOAD", df.to_csv(index=False).encode(), filename, use_container_width=True)
                st.markdown("---")
# DASHBOARD
elif choice == 'Dashboard of the data':
    st.markdown("<h1 style='color:#ffd700;text-align:center;'>DASHBOARD – DATA ANALYSIS</h1>", unsafe_allow_html=True)
    
    # On récupère toutes les données déjà scrapées
    dfs = []
    if st.session_state.df_men_clothes is not None:
        dfs.append(st.session_state.df_men_clothes)
    if st.session_state.df_kids_clothes is not None:
        dfs.append(st.session_state.df_kids_clothes)
    if st.session_state.df_men_shoes is not None:
        dfs.append(st.session_state.df_men_shoes)
    if st.session_state.df_kids_shoes is not None:
        dfs.append(st.session_state.df_kids_shoes)
    
    if not dfs:
        st.error("Scrap at least one category first!")
        st.stop()
    
    df_all = pd.concat(dfs, ignore_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df_all, x="price", color="type", title="Price Distribution", color_discrete_sequence=['#ff6b6b', '#4ecdc4'])
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.box(df_all, x="type", y="price", color="type", title="Price Boxplot", color_discrete_sequence=['#ff9ff3', '#54a0ff'])
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        top_cities = df_all['address'].value_counts().head(10)
        fig3 = px.bar(y=top_cities.index, x=top_cities.values, orientation='h', title="Top 10 Cities", color=top_cities.values)
        st.plotly_chart(fig3, use_container_width=True)

        avg_price = df_all.groupby('address')['price'].mean().sort_values(ascending=False).head(10)
        fig4 = px.bar(x=avg_price.index, y=avg_price.values, title="Most Expensive Cities", color=avg_price.values)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"<h3 style='text-align:center;color:white;'>Total: {len(df_all):,} products</h3>", unsafe_allow_html=True)

#  EVALUATE 
else:
    st.markdown("<h2 style='text-align:center;color:#ffd700;margin-bottom:50px;'>Evaluate the App</h2>", unsafe_allow_html=True)
    

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("KoboToolbox", use_container_width=True):
            st.markdown('<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/x/xJdf7vmv">', unsafe_allow_html=True)
        
        if st.button("Google Forms", use_container_width=True):
            st.markdown('<meta http-equiv="refresh" content="0; url=https://docs.google.com/forms/d/e/1FAIpQLSc5-X5Ef-WZr-b6e_huLqINK-IAFvEq_Q_fiAl2035OcFzMMQ/viewform">', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:white;font-size:20px;font-weight:bold;'>NGUEMTCHUENG TSEMO BIBIANE DANIELLE<br>December 2025 • Senegal</p>", 
            unsafe_allow_html=True)