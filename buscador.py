import streamlit as st
import requests
import psycopg2
import os

def conectar_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, sslmode='require')

st.set_page_config(page_title="Buscador Precios AR", layout="wide")

st.title("🔎 Buscador de Supermercados (Argentina)")
query = st.text_input("Buscar por nombre o EAN:")

if query:
    url = "https://d3e6htiiul5ek9.cloudfront.net/prod/productos"
    params = {"string": query, "lat": -34.60, "lng": -58.38, "limite": 15}
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.preciosclaros.gob.ar/"}
    
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        productos = res.json().get('productos', [])
        for p in productos:
            with st.container():
                c1, c2, c3 = st.columns([1, 4, 1])
                img_url = f"https://imagenes.preciosclaros.gob.ar/productos/{p['id']}.jpg"
                c1.image(img_url, width=80)
                c2.write(f"**{p['nombre']}** ({p['marca']})")
                c2.caption(f"EAN: {p['id']} | Precio: ${p['precioMax']}")
                
                if c3.button("Agregar", key=p['id']):
                    conn = conectar_db()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO mis_productos (producto, marca, ean_codigo, categoria, imagen, precio, fuente, fecha)
                        VALUES (%s, %s, %s, %s, %s, %s, 'Precios Claros', CURRENT_TIMESTAMP)
                        ON CONFLICT (ean_codigo) DO UPDATE SET precio = EXCLUDED.precio, fecha = CURRENT_TIMESTAMP;
                    """, (p['nombre'], p['marca'], p['id'], 'General', img_url, p['precioMax']))
                    conn.commit()
                    st.success("¡Agregado!")
