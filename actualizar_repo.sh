#!/bin/bash

# Navegar al directorio del repositorio
cd /home/pi/culodewecho/

# Ejecutar el script para generar la lista de canales
python3 extraer_acestream.py

# Agregar los cambios al repositorio
git add lista_canales.txt
git commit -m "Actualización automática de la lista de canales ($(date))"

# Subir los cambios a GitHub
git push origin main
