# database.py

import sqlite3
import pandas as pd
import os

if not os.path.exists("data"):
    os.makedirs("data")

DB_PATH = "data/cleaned_data.db"

def sauvegarder(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("produits", conn, if_exists="replace", index=False)
    conn.close()
    

def charger():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM produits", conn)
    conn.close()
    return df

def existe():
    return os.path.exists(DB_PATH)