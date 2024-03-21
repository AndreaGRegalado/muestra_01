# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:45:31 2024

@author: andrea.garcia
"""

import netCDF4 as nc
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import datetime
import matplotlib.dates as mdates


# RUTA ABSOLUTA
#ruta_archivo = r"C:\Users\andre\scripts\python\datos\sst.day.mean.2024.nc"

# RUTA RELATIVA, lee la ruta donde está el script. El nc tiene que estar ahí, en carpeta datos.
directorio_actual = os.getcwd()

archivo = "datos\sst.day.mean.2024.nc"

# Crea la ruta al directorio padre (una carpeta atrás)
directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
ruta_archivo = os.path.join(directorio_padre,archivo)
    
       
# Abre el archivo NetCDF con xarray
print(ruta_archivo)
ds = xr.open_dataset(ruta_archivo, decode_cf=False)


# Calcula la media de la SST a lo largo del tiempo
sst_mean = ds.sst.mean(dim='time')

# Coordenadas de la boya AGL
boya_AGL = (-3.784, 43.894)

# Rango de niveles para el mapa
levs = np.arange(10, 20, 0.1)


# Crear figura y subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subgráfico 1: Mapa
ax1 = plt.subplot(1, 2, 1, projection=ccrs.Mercator())

# Agrega los datos de SST media al mapa
mapa = ax1.contourf(ds.lon, ds.lat, sst_mean,
                    levs,
                    cmap='jet',
                    transform=ccrs.PlateCarree(),
                    extend='both')

# Agrega color beige a la tierra
ax1.add_feature(cfeature.LAND, color='beige')

# Agrega las líneas de costa y la cuadrícula
ax1.coastlines()
grid = ax1.gridlines(draw_labels=True)
grid.bottom_labels = False
grid.right_labels = False

plt.colorbar(mapa,
            ax=ax1,  # Indica el eje al que se añadirá la barra de color
            label="°C",  # Etiqueta del colorbar
            shrink=0.5)

# Agrega el punto de la boya
ax1.scatter(boya_AGL[0], boya_AGL[1],
            color='red',
            marker='o',
            transform=ccrs.PlateCarree())

# Agrega texto en el punto especificado
ax1.text(boya_AGL[0] + 0.1, boya_AGL[1] + 0.15,
        'Boya AGL',
        color='black',
        fontsize=12,
        transform=ccrs.PlateCarree())

# Define los límites de la región que deseas mostrar
lon_min, lon_max = -12, 0
lat_min, lat_max = 40, 48

# Establece los límites de la región en los ejes
ax1.set_extent((lon_min, lon_max, lat_min, lat_max))
ax1.set_title("SST 2024")

# Subgráfico 2: Línea temporal. Pasar primero lon y luego lat. Como los datos de lon tiene rango de 0-360, 
#hay que  pasarle % 360, le suma 360 grados repetidamente hasta que la longitud sea positiva y esté en el rango de 0 a 360 grados. Si ya es +, no hace nada
#ax2.plot(ds.time(), ds.sst.sel(lon = -3.78 % 360, lat = 43.89, method='nearest'), color='blue')
#fechas_dia_mes = ds.time.dt.strftime('%d-%m-%Y')
ax2.plot(ds.time, ds.sst.sel(lon = -3.78 % 360, lat = 43.89, method='nearest'), color='blue')
ax2.set_xlabel('Fecha')
myFmt = mdates.DateFormatter('%d-%b')
ax2.xaxis.set_major_formatter(myFmt)

#Para que pinte en spyder, quitar este xlim
"""# Establecer los límites del eje x
inicio = datetime.datetime(2024, 1, 1)
fin = datetime.datetime(2024, 4, 1)
ax2.set_xlim([inicio, fin])"""

ax2.set_ylabel('Temperatura (°C)')
ax2.legend()
ax2.set_title('Serie Temporal Boya AGL (2024)')
ax2.grid()

# Ajustar diseño y mostrar el gráfico
plt.tight_layout()
plt.show()



