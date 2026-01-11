import streamlit as st
import requests
import psycopg2

def conectar_db():
    return psycopg2.connect(dbname="tu_db", user="tu_usuario", password="tu_pass", host="localhost")

st.set_page_config(page_title="Gestor de Precios", layout="wide")
st.title("🔎 Buscador y Agregador de Productos")

query = st.text_input("Buscar por nombre o EAN (ej: 'leche' o '779...')")

if query:
    url = "https://d3e6htiiul5ek9.cloudfront.net/prod/productos"
    # Lat/Lng de Ramos Mejía/CABA por defecto
    params = {"string": query, "lat": -34.66, "lng": -58.56, "limite": 15}
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.preciosclaros.gob.ar/"}
    
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        productos = res.json().get('productos', [])
        
        for p in productos:
            with st.container():
                col1, col2, col3 = st.columns([1, 4, 1])
                
                # Imagen del producto (la API usa el EAN para la URL de imagen)
                img_url = f"https://imagenes.preciosclaros.gob.ar/productos/{p['id']}.jpg"
                col1.image(img_url, width=100)
                
                col2.write(f"**{p['nombre']}**")
                col2.caption(f"Marca: {p['marca']} | EAN: {p['id']}")
                col2.write(f"Precio Actual: **${p['precioMax']}**")
                
                if col3.button("Monitorear", key=p['id']):
                    try:
                        conn = conectar_db()
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT INTO mis_productos (producto, marca, ean_codigo, categoria, imagen, precio, fecha)
                            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                            ON CONFLICT (ean_codigo) DO UPDATE SET 
                                precio = EXCLUDED.precio,
                                fecha = CURRENT_TIMESTAMP;
                        """, (p['nombre'], p['marca'], p['id'], "General", img_url, p['precioMax']))
                        conn.commit()
                        st.success("Guardado")
                        cur.close()
                        conn.close()
                    except Exception as e:
                        st.error(f"Error: {e}")
