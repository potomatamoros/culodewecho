import requests
import re
from bs4 import BeautifulSoup

# Función para extraer los canales de la página HTML
def extraer_canales(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar los canales (asumiendo que están en una lista <li>)
    canales = []
    for div in soup.find_all('div', class_='link-name'):
        nombre = div.text.strip()
        enlace = div.find_next('a')['href']  # Enlace de AceStream

        # Obtener el logo (si está en un <img>)
        logo = div.find_previous('img')['src'] if div.find_previous('img') else None

        canales.append({
            'nombre': nombre,
            'enlace': enlace,
            'logo': logo
        })
    return canales

# Función para obtener el EPG desde el archivo de GitHub
def obtener_epg():
    url = 'https://raw.githubusercontent.com/davidmuma/Canales_dobleM/master/Varios/EPG/General.md'
    response = requests.get(url)
    return response.text

# Extraer los canales
url_pagina_canales = 'URL_DE_TU_PAGINA_CON_CANALES'  # Reemplaza con la URL de tu página
canales = extraer_canales(url_pagina_canales)

# Obtener el EPG (programación de canales)
epg_data = obtener_epg()

# Parsear el EPG (por ejemplo, extraer la programación de cada canal)
# Esto depende del formato del EPG, por lo que necesitarás ajustar esta parte según sea necesario
epg_dict = {}
for linea in epg_data.splitlines():
    if linea.startswith('#'):
        canal_name = linea[1:].strip()  # Nombre del canal
        epg_dict[canal_name] = []
    else:
        epg_dict[canal_name].append(linea.strip())  # Programación del canal

# Crear el archivo M3U
with open("/home/pi/culodewecho/lista_canales.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    # Escribir los canales con su información
    for canal in canales:
        nombre_canal = canal['nombre']
        enlace = canal['enlace']
        logo = canal['logo']
        epg = "\n".join(epg_dict.get(nombre_canal, []))  # Obtener el EPG si existe

        # Si el logo está disponible, incluirlo en el encabezado
        f.write(f'#EXTINF:-1 tvg-logo="{logo}" tvg-name="{nombre_canal}" group-title="General", {nombre_canal}\n')
        f.write(f'{enlace}\n')

print("Extracción completada. Los resultados están en 'lista_canales.m3u'.")
