# -*- coding: utf-8 -*-


"""
    Programa de lectura de los sensores del SMART-WATER y escritura de los mismos en la base de datos SQLite.
    El programa se conecta al puerto serie USB0 de la Raspberry, le da formato al string que recibe y extrae
    los valores de los sensores que encuentra.


"""

import os, sys
import serial
import time
import sqlite3
import signal
from datetime import datetime

# Variable que establece si el programa tiene que continuar o no #
keep_going = True

def manejador_de_senal(signum, frame):
    global keep_going
    # Si entramos en el manejador por una llamada CTRL-C, ponemos el flag a False
    keep_going = False
signal.signal(signal.SIGTERM,manejador_de_senal)       

# Crea un objeto serie con la dirección, baudrate, tiempo de espera (este último se modifica de 5 a 7 para que de
# tiempo de lectura y no retorne line en blanco o erro de lectura)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 7)
ser.flushInput() # Vaciamos el buffer de recepcion #

# Esperamos 7 segundos para comenzar a leer para asegurarnos de que el buffer este lleno
time.sleep(7)

# nos conectamos con la base de datos llamada prueba1.db
conectar=sqlite3.connect("prueba1.db")

# creamos un cursor que nos permitirá interactuar con la base de datos
cursor=conectar.cursor()

# Creamos el diccionario que contiene los valores de las variables #
variables = {}

# Numero de intentos fallidos maximos antes de terminar el proceso #
intentos_max = 10
intentos = 0

while keep_going:

    # Leemos del puerto serie
    line = ser.readline()

    if len(line) == 0: # mensaje no se ha recibido aun
        print("Time out! Trying again.\n")
        intentos += 1 # Sumamos un intento fallido
        if intentos == intentos_max: # Si llegamos al numero maximo, terminamos el proceso
            keep_going = False
            print("WARNING: NUMERO DE INTENTOS MAXIMOS SUPERADOS. TEMRINANDO PROCESO.")

    else:

        # Recibimos informacion, reseteamos el numero de intentos
        intentos = 0

        # Pasamos a cadena de caracteres #
        line_str = str(line)

        if len(line_str) < 10:
            print("La linea que se ha leido tiene un formato desconocido o viene corrupto.")
            continue

        # Dividimos entre campos
        # Formato de paquete ION: #
        # line_str = [JUNK, JUNK, ID, SAMPLE_NUM, BATM, TEMP, PH, DO, COND, ORP, eop]
        # Formato de paquete no-ION: #
        # line_str = [JUNK, JUNK, ID, SAMPLE_NUM, BATM, TEMP, PH, COND, ORP, eop]

        line_str = line_str.split('#')
        # Descartamos los dos primeros campos y el ultimo (JUNK)
        line_str = line_str[2:-1]

        # La línea de código anterior separa los caracteres del principio de la lectura que "no tienen"
        # importancia en la lectura de los sensores
        # Se han identificado y separado las partes que interesan de la cadena, es decir, se intenta eliminar
        # o separar los caracteres que no se interpretan como parte de los sensore

        # Iteramos para cada uno de los valores en la cadena #
	print(line_str)
        variables['DO'] = -1.0  # Como no es seguro que el SW tenga este sensor, le damos un valor -1 predeterminado.

        for indx, campo in enumerate(line_str):

            if indx == 0:  # El primer campo no es un sensor, es el nombre del SW
                variables['ID'] = campo
            elif indx == 1:  # El segundo campo tampoco es un sensor, es el numero de muestra #
                variables['SAMPLE_NUM'] = campo
            else:  # El resto si son sensores
                sensor, valor = campo.split(':')  # Cada campo de line_str tiene como formato "SENSOR:VALOR"
                variables[sensor] = float(valor)  # Almacenamos el valor leido en el campo que indica el nombre sensor

        str_date = str(datetime.now()) # Leemos la fecha y la convertimos en string
        # Metemos la fecha en el diccionario de variables
        variables['DATE'] = str_date

        #creamos una tupla de parámetros que nos permitirá introducir los datos en la tabla sensor
        parametros=(variables['ID'],
                    variables['SAMPLE_NUM'],
                    variables['BAT'],
                    variables['WT'],
                    variables['PH'],
                    variables['DO'],
                    variables['COND'],
                    variables['ORP'],
                    variables['DATE'])

        #insertamos valores en nuestra tabla "sensor"
        cursor.execute("INSERT INTO sensor (ID,SAMPLE_NUM,BAT,TEMP,PH,DO,COND,ORP,DATE) VALUES(?,?,?,?,?,?,?,?,?)", parametros)
        
        # el siguiente comando "commit()" guarda la tabla creada
        conectar.commit()

# Cuando salgamos del bucle While debido a una senal de interrupcion asincrona, cerramos elegantamente los procesos
print("Cerrando base de datos!")
conectar.close() # Cerramos la DB
print("Base de datos cerrada")
print("Cerrando puerto serie!")
ser.close() # Cerramos la com. serie
print("Puerto serie cerrado!")
exit() # Salimos del programa

