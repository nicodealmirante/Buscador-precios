import requests
import psycopg2
import os
import time
import schedule

def job_actualizacion():
    print("Iniciando actualización diaria...")
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    
    cur.execute("SELECT ean_codigo FROM mis_productos")
    items = cur.fetchall()
    
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.preciosclaros.gob.ar/"}
    
    for (ean,) in items:
        url = "https://d3e6htiiul5ek9.cloudfront.net/prod/productos"
        params = {"string": ean, "lat": -34.60, "lng": -58.38}
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            data = r.json().get('productos', [])
            if data:
                nuevo_precio = data[0]['precioMax']
                cur.execute("UPDATE mis_productos SET precio = %s, fecha = CURRENT_TIMESTAMP WHERE ean_codigo = %s", (nuevo_precio, ean))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Actualización completada.")

# Programación: cada día a las 09:00 AM
schedule.every().day.at("09:00").do(job_actualizacion)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
