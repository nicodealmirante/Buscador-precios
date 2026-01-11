import requests
import psycopg2
import os

# Lista de productos que quieres agregar inicialmente
# Puedes poner nombres ('Leche') o EANs ('7790123456789')
PRODUCTOS_A_CARGAR = ["Aceite De Girasol 1.5 L Natura",
"Aceite De Girasol Cañuelas 900 Ml",
"Aceite Girasol Legítimo 900 Ml",
"Aceitunas Castell Descarozadas 150 Gr",
"Acondicionador Rizos Definidos 190 Ml Sedal",
"Acondicionador Prebióticos Biotina 340 Ml Sedal",
"Aderezo Ketchup Natura 250 Gr",
"Alfajor Blanco Jorgito 30 G",
"Almohada Espuma Baja Densidad 60x40",
"Arroz Dos Hermanos 1kg",
"Azúcar Ledesma 1kg",
"Bolsa De Consorcio X10 Unidades",
"Caldo Knorr Gallina X2",
"Caramelo Arcor X 100g",
"Cerveza Andes Rubia Lata 473 Ml",
"Coca Cola 1.5 L",
"Colgate Triple Acción",
"Conservadora Plástica Chica 6lts",
"Desodorante Dove 150 Ml",
"Desodorante Nivea Black&White 150 Ml",
"Detergente Magistral Limón 750ml",
"Fideos Spaghetti Marolio 500 Gr",
"Galletitas Criollitas 3 Paq",
"Galletitas Pepitos Mini Arcor",
"Jabón En Pan Ala 3 Unidades",
"Jabón Líquido Para Ropa Ala 800 Ml",
"Jabón Tocador Dove 90 Gr",
"Lavandina Ayudín 1lt",
"Mayonesa Natura 250 Gr",
"Mermelada La Campagnola Durazno 390gr",
"Pan De Molde Fargo",
"Papel Higiénico Higienol 4 Rollos",
"Pre Pizza X2",
"Queso Untable Mendicrim 290gr",
"Sal Fina Dos Anclas 500gr",
"Salsa Lista Fileto Arcor 340 Gr",
"Shampoo Sedal Rizos 190ml",
"Shampoo Sedal Biotina 340ml",
"Toalla De Mano",
"Turrón Arcor Blanco",
"Yogur Bebible Ilolay Frutilla 1 Lt",
"Yerba Taragüi 1kg",
"Fideos Codito Marolio 500 Gr",
"Fideos Mostachol Lucchetti 500 Gr",
"Sopa Instantánea Knorr Pollo",
"Sopa Instantánea Knorr Verdura",
"Arvejas Secas Ledesma 500 Gr",
"Lentejas Ledesma 500 Gr",
"Leche Entera La Serenísima 1lt",
"Leche Descremada Ilolay 1lt",
"Queso Rallado La Paulina 40 Gr",
"Crema De Leche Milkaut 200cc",
"Chocolate Águila Barra 100 Gr",
"Gelatina Exquisita Frutilla",
"Flan Casero Exquisita",
"Té Verde Taragüi",
"Yerba Rosamonte 1kg",
"Yerba La Tranquera 500gr",
"Galletitas Lincoln 3 Paq",
"Chocolinas X 2 Paq",
"Alfajor Negro Fantoche Triple",
"Caramelos Sugus Bolsa 100g",
"Galletitas Express Arcor",
"Tostadas Fargo 200 Gr",
"Pan Lactal Lino",
"Pan Rallado Lucchetti 500gr",
"Arroz Largo Fino Molto",
"Azúcar Dominó 1kg",
"Sal Gruesa Dos Anclas 1kg",
"Vinagre De Alcohol Menoyo 1lt",
"Aceite De Oliva Zuelo 500ml",
"Mostaza Natura 250 Gr",
"Mayonesa Hellmann’s 250 Gr",
"Salsa Golf Natura 250 Gr",
"Ketchup Heinz 397 Gr",
"Chimichurri Listo 220 Gr",
"Puré De Tomate Arcor 520gr",
"Tomate Triturado La Campagnola 500gr",
"Pickles Agridulces Arcor",
"Choclo Amarillo Entero Lata",
"Atún Desmenuzado En Agua La Campagnola",
"Caballa Al Natural Arcor",
"Harina 0000 Pureza 1kg",
"Harina Leudante Blancaflor 1kg",
"Polenta Mágica Mágica 500 Gr",
"Premezcla Sin Tacc Fargo 400 Gr",
"Chocolate En Polvo Toddy 200 Gr",
"Cacao En Polvo Nesquik 180 Gr",
"Leche Condensada Nestlé Lata",
"Postre Royal Chocolate",
"Manteca Sancor 200 Gr",
"Margarina Dorina 200 Gr",
"Café Instantáneo Nescafé 100 Gr",
"Café Torrado Molido La Virginia 250 Gr",
"Yerba CBSe Hierbas Serranas 500 Gr",
"Infusión Capuccino Arlistan",
"Mate Cocido Taragüi Saquitos",
"Té Negro La Virginia 50 Saquitos",
"Jugo En Polvo Clight Naranja",
"Jugo En Polvo Tang Pomelo",
"Jugo En Polvo Arcor Multifruta",
"Agua Saborizada Levité Manzana 1.5 L",
"Agua Mineral Eco De Los Andes 2.25 L",
"Gaseosa Sprite 1.5 L",
"Gaseosa Fanta Naranja 1.5 L",
"Pack Cerveza Quilmes Lata X 6",
"Vino Tinto Uvita 750 Ml",
"Vino Blanco Toro 1lt",
"Fernet Branca 750 Ml",
"Gin Bosque Alta Montaña",
"Vodka Smirnoff 700ml",
"Ron Havana Club 750 Ml",
"Whisky Jameson 750 Ml",
"Jabón En Barra Zorro 3 Unid",
"Shampoo Plusbelle Familiar",
"Crema Dental Sensodyne 90 Gr",
"Toalla Higiénica Always Noches Tranquilas",
"Pañales Pampers XG X 10",
"Pañales Huggies Classic G X 20",
"Protector Diario Carefree 20 Unid",
"Algodón Hidrófilo 100 Gr",
"Hisopos Johnson’s X 75",
"Desodorante Axe Dark Temptation",
"Desodorante Rexona Clinical",
"Limpiador Poett Lavanda 900ml",
"Desinfectante Ayudín Aerosol",
"Escoba De Paja Nacional",
"Trapo De Piso Reforzado",
"Esponja Multiuso X2",
"Jabón Líquido Para Manos Dove",
"Toalla De Cocina Scott 2 Rollos",
"Papel Higiénico Elite 4 Rollos",
"Servilletas Elite X 100",
"Bolsa De Basura 20lts X10",
"Baldes Plásticos Con Asa",
"Perchas Plásticas Pack X6",
"Almohada Alta Densidad 70x50",
"Sábanas 1 Plaza 100% Algodón",
"Sábanas 2 Plazas Estampadas",
"Toallón Playero 140x70",
"Rollo De Cocina Sussex 3 Rollos",
"Limpiador Cif Crema 500ml",
"Ambientador Glade Lavanda",
"Pastilla Para Inodoro Pato",
"Desodorante De Ambiente Poett Aerosol",
"Espuma De Afeitar Gillette",
"Cepillo De Dientes Oral B Suave",
"Enjuague Bucal Listerine",
"Protector Solar Nivea FPS 50",
"Crema Humectante Pond’s",
"Desodorante Dove Dermoaclarant",
"Shampoo Tío Nacho Engrosador",
"Shampoo Head & Shoulders",
"Shampoo Pantene Liso Extremo"]

def conectar_db():
    # En Railway esto lee la variable automáticamente
    url = os.getenv('DATABASE_URL')
    return psycopg2.connect(url, sslmode='require')

def ejecutar_carga():
    conn = conectar_db()
    cur = conn.cursor()
    
    # Headers más completos para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.preciosclaros.gob.ar/",
        "Accept": "application/json, text/plain, */*",
        "x-requested-with": "XMLHttpRequest"
    }

    for item in LISTA_PRODUCTOS:
        print(f"Buscando: {item}...")
        # Usamos coordenadas del centro de CABA para asegurar resultados
        url = "https://d3e6htiiul5ek9.cloudfront.net/prod/productos"
        params = {
            "string": item,
            "lat": -34.6037,
            "lng": -58.3816,
            "limite": 1
        }

        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            data = r.json()
            productos = data.get('productos', [])

            if productos:
                p = productos[0]
                ean = p['id']
                nombre = p['nombre']
                marca = p['marca']
                precio = p['precioMax']
                img = f"https://imagenes.preciosclaros.gob.ar/productos/{ean}.jpg"
                
                cur.execute("""
                    INSERT INTO mis_productos (ean_codigo, producto, marca, categoria, imagen, precio, fuente, fecha)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Precios Claros', CURRENT_TIMESTAMP)
                    ON CONFLICT (ean_codigo) DO UPDATE SET 
                        precio = EXCLUDED.precio, 
                        fecha = CURRENT_TIMESTAMP;
                """, (ean, nombre, marca, 'General', img, precio))
                print(f"✅ Guardado: {nombre} - ${precio}")
            else:
                print(f"❌ No se encontró nada para: {item}")
        
        except Exception as e:
            print(f"Error con {item}: {e}")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ejecutar_carga()

if __name__ == "__main__":
    # Asegúrate de tener la variable DATABASE_URL configurada en tu terminal
    # o corre esto dentro de Railway
    cargar_lista()
