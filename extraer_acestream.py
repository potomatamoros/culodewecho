import re

# Leer el archivo HTML
with open("/home/pi/culodewecho/pagina.html", "r", encoding="utf-8") as f:
    contenido = f.read()

# Expresión regular para extraer los nombres de los canales y los enlaces de AceStream
patron = r'<div class="link-name">(.*?)</div>.*?href="(acestream://[^"]+)"'

# Buscar todas las coincidencias
canales = re.findall(patron, contenido)

# Crear el archivo .m3u
with open("/home/pi/culodewecho/lista_canales.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")  # Cabecera del archivo M3U

    # Escribir los canales y sus URLs en el formato correcto
    for canal in canales:
        nombre, url = canal
        f.write(f"#EXTINF:-1, {nombre}\n")
        f.write(f"{url}\n")

print("Extracción completada. Los resultados están en 'lista_canales.m3u'.")

