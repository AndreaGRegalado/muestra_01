# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 11:31:40 2024

PEDRO. Para actualizar datos de la noaa, descarga los del año, con el ultimo dato
disponible

@author: andrea.garcia
"""
from ftplib import FTP
import datetime
import os
import xarray as xr

#ruta_archivo = r'C:\Users\andre\scripts\python\datos'

# RUTA RELATIVA, decirle donde guardarlo, en carpeta "datos" de la ruta donde está el script
directorio_actual = os.getcwd()

data_dir = "datos"

# Crea la ruta al directorio padre (una carpeta atrás)
directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))
ruta_archivo = os.path.join(directorio_padre,data_dir)

year = datetime.date.today().year
fileThisYear = 'sst.day.mean.'+str(year)+'.nc'

#Para acceder a un archivo que está en otra dirección al script
#os.chdir(ruta_archivo)

print('>>>>> Descargando datos '+fileThisYear+' en '+ruta_archivo)

ftp = FTP('ftp.cdc.noaa.gov')  # connect to host, default port
ftp.login()  
ftp.cwd('Datasets/noaa.oisst.v2.highres/');

with open(os.path.join(ruta_archivo, fileThisYear), 'wb') as f:
    ftp.retrbinary("RETR " + fileThisYear, f.write)
ftp.quit();

print('>>>>> Datos descargados '+fileThisYear+' en '+ruta_archivo)

os.chdir(directorio_actual)

DS = xr.open_dataset(ruta_archivo+'/'+fileThisYear)
print('>>>>> Ultimo dato: '+DS.time[-1].dt.strftime("%d %B %Y").values)








