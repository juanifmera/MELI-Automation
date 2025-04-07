# ----------------------------- #
# Web Scraping de MercadoLibre #
# Conversión a dólares MEP     #
# ----------------------------- #

from bs4 import BeautifulSoup
import requests
import pandas as pd

# --------------------- PARTE 1: Construcción del link de búsqueda ---------------------

# Separadores para construir la URL de búsqueda
separator1 = '-'
separator2 = '%'

# Ingreso del nombre del producto
product_to_by = input('¿Qué artículo deseas buscar? ').lower().split(' ')

# Generamos la URL compatible con la estructura de Mercado Libre
product_search = f'{separator1.join(product_to_by)}#D[A:{separator2.join(product_to_by)}]'
url_mercado_libre = f'https://listado.mercadolibre.com.ar/{product_search}'

# Realizamos la petición HTTP a Mercado Libre
result1 = requests.get(url_mercado_libre)

# --------------------- PARTE 2: Obtener la cotización del dólar MEP ---------------------

url_dolar_hoy = 'https://dolarhoy.com/'
result2 = requests.get(url_dolar_hoy)

if result2.status_code == 200:
    soup_dolar = BeautifulSoup(result2.text, 'html.parser')
    
    # El índice [7] corresponde al valor del dólar MEP en la estructura actual del HTML
    dolar_mep = soup_dolar.find_all('div', class_='val')
    valor_mep = float(str(dolar_mep[7].string).split('$')[1].replace(',', '.'))

else:
    print(f'Hubo un error en la petición a la página de DolarHoy. Error: {result2.status_code}')

# --------------------- PARTE 3: Web Scraping de Mercado Libre ---------------------

if result1.status_code == 200:
    soup = BeautifulSoup(result1.text, 'html.parser')

    # Listas donde guardamos los datos del scraping
    titles_list = []
    prices_list = []
    links_list = []
    rating_list = []

    # Función para limpiar los precios (eliminar separadores y convertir a int)
    def clean_price(price):
        try:
            cleaned_price = int(price.replace('.', '').replace(',', ''))
            return cleaned_price
        except (ValueError, AttributeError):
            return 0

    # Buscamos todas las tarjetas de productos
    info = soup.find_all('div', class_='poly-card__content')

    for x in info:
        # Título del producto
        titles_list.append(x.find('h2').string)
        
        # Link al producto
        links_list.append(x.find('a')['href'])

        # Rating del producto
        rating = x.find('span', class_='andes-visually-hidden')
        rating_list.append(rating.string if rating else 'No Rating')

        # Lógica para identificar y limpiar el precio según la estructura del HTML
        if x.find('s', class_='andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma'):
            # Precio con descuento
            discounted_price = x.find('span', class_='andes-money-amount__fraction').find_next('span', class_='andes-money-amount__fraction').string
            cleaned_price = clean_price(discounted_price)
        else:
            # Precio regular o alternativo
            price = x.find('span', class_='andes-money-amount__fraction').string
            cleaned_price = clean_price(price)

        prices_list.append(cleaned_price)

        # Asegurarse de que todas las listas estén sincronizadas en longitud
        min_length = min(len(titles_list), len(prices_list), len(links_list), len(rating_list))
        titles_list, prices_list, links_list, rating_list = (
            titles_list[:min_length],
            prices_list[:min_length],
            links_list[:min_length],
            rating_list[:min_length],
        )

    # --------------------- PARTE 4: Creación del DataFrame ---------------------

    # Creamos el DataFrame con los primeros 20 resultados
    mercado_libre_df = pd.DataFrame({
        'Title': titles_list[:20],
        'Price (in Pesos)': prices_list[:20],
        'Rating': rating_list[:20],
        'Link': links_list[:20]
    })

    # Ordenamos por precio
    mercado_libre_sorted = mercado_libre_df.sort_values(by='Price (in Pesos)')

    # Agregamos columna con precio en dólares MEP
    mercado_libre_sorted['Price (in USD MEP Dolars)'] = round(mercado_libre_sorted['Price (in Pesos)'] / valor_mep, 2)

    # Formateamos los precios para mayor legibilidad
    mercado_libre_sorted['Price (in USD MEP Dolars)'] = mercado_libre_sorted['Price (in USD MEP Dolars)'].apply(lambda x: "{:,}".format(x).replace(',', '.'))
    mercado_libre_sorted['Price (in Pesos)'] = mercado_libre_sorted['Price (in Pesos)'].apply(lambda x: "{:,}".format(x).replace(',', '.'))

    # Reordenamos las columnas
    columns_order = ['Title', 'Price (in Pesos)', 'Price (in USD MEP Dolars)', 'Rating', 'Link']
    mercado_libre_sorted = mercado_libre_sorted[columns_order]

    # --------------------- PARTE 5: Exportar a Excel ---------------------

    file_name = input('¿Cómo querés que se llame tu archivo? ')
    file_path = f'C:/Users/juani/OneDrive/Documentos/Python/11_Automation/{file_name}.xlsx'
    
    mercado_libre_sorted.to_excel(file_path, index=False, sheet_name='Mercado Libre')
    print("✅ Archivo guardado correctamente.")

else:
    print(f'❌ Hubo un error con la petición a la página de Mercado Libre. Código: {result1.status_code}')
