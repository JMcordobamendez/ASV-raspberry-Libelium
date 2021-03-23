import os, sys
#import serial
import time
import sqlite3
import signal
import subprocess as sub
from datetime import datetime
#Compruebo que la base de datos existe, si no, procedo a crearla (nos ahorramos el script que crea la base de datos)
def existe():
    iniciar = True
    directorio = str(sub.check_output(["ls"], shell=True)) #me lee lo que tengo en el directorio
    directorio = directorio.split("'")
    directorio = directorio[1]
    directorio = directorio.split("\\n")
    for n in directorio: #recorro todo lo que tengo en el directorio para asegurarme de que existe prueba1.db

        if n == "prueba1.db": #que existe
            iniciar = False #no me hagas el siguiente condicional
            break

    if iniciar == True:
        # instala el programa sqlite3 en el ordenador
        sub.run(['sudo apt-get install sqlite3'], shell=True)
        # nos conectamos con la base de datos llamada prueba1.db
        # si no existe crea una con ese nombre en el mismo directorio
        conectar = sqlite3.connect("prueba1.db")
        # Creamos un cursor que nos permitirá interactuar con la base de datos
        cursor = conectar.cursor()
        # ahora creamos la tabla con los datos que guardaremos
        cursor.execute("""CREATE TABLE sensor(
                        ID text,
                        SAMPLE_NUM real,
                        BAT real,
                        TEMP real,
                        PH real,
                        DO real,
                        COND real,
                        ORP real,
                        DATE string
                        )""")
        # el siguiente comando "commit()" guarda la tabla creada
        conectar.commit()

        # cerramos la conexión con la base de datos
        conectar.close()

        # cambiamos los permisos de la base de datos para permitir lectura y escritura
        sub.run(['sudo chown pi prueba1.db'], shell=True)

        # instala la librería pyserial en python3 necesaria para leer datos por puerto serie
        sub.run(['sudo pip3 install pyserial'], shell=True)
#inicializamos la función anterior
existe()
import serial
#con el número de serie, localizo en que puerto USB está conectado el dispositivo y luego pregunto a qué "ttyUSB*" corresponde
puerto = str(sub.check_output(["numserie='AH0644B8' ; dmesg | grep $(dmesg | grep $numserie | tail -1 | awk '{print $4}') | tail -1 | awk '{print $13}'"], shell=True))
puerto = puerto.split("'")
puerto = puerto[1]
puerto = puerto.split("\\")
puerto = puerto[0] #ya sabemos el puerto "ttyUSB" al que corresponde

#Crea un objeto serie con la dirección, baudrate, tiempo de espera (este último se modifica de 5 a 7 para que de tiempo de lectura y no retorne line en blanco o erro de lectura)
if puerto == "ttyUSB0":
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=6)
elif puerto == "ttyUSB1":
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=6)
elif puerto == "ttyUSB2":
    ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=6)
elif puerto == "ttyUSB3":
    ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=6)
else:
    exit("The device with the SerialNumber: AH0644B8 is not connected")

ser.reset_input_buffer() # Vaciamos el buffer de recepcion #

# Esperamos 7 segundos para comenzar a leer para asegurarnos de que el buffer este lleno
time.sleep(6)

#nos conectamos con la base de datos llamada prueba1.db
conectar = sqlite3.connect("prueba1.db")

#creamos un cursor que nos permitirá interactuar con la base de datos
cursor = conectar.cursor()

# Variable que establece si el programa tiene que continuar o no #
keep_going = True

def manejador_de_senal(signum, frame):
    global keep_going
    # Si entramos en el manejador por una llamada CTRL-C, ponemos el flag a False
    keep_going = False
signal.signal(signal.SIGTERM,manejador_de_senal)

def Basedatos (Datos):
    # Leemos del puerto serie
    time.sleep(0.5)
    line = ser.read(ser.in_waiting)

    if line == b'':  # He leido un buffer vacio
        '''
        print("Buffer vacio. Esperando recepcion")
        '''

    else:

        tramas = str(line)  # Pasamos a string
        tramas = tramas.split('<=>')  # Dividimos entre tramas

        #if len(tramas) < 2:
         #   continue


        trama = tramas[1]  # Cogemos la primera trama del buffer

        # Dividimos entre campos
        # Formato de paquete ION: #
        # line_str = [JUNK, JUNK, ID, SAMPLE_NUM, BATM, TEMP, PH, DO, COND, ORP, eop]
        # Formato de paquete no-ION: #
        # line_str = [JUNK, JUNK, ID, SAMPLE_NUM, BATM, TEMP, PH, COND, ORP, eop]

        line_str = trama.split('#')

        if len(line_str) > 11:
            print('ERROR DE FORMATO')
            #continue

            # Descartamos los dos primeros campos y el ultimo (JUNK)
        line_str = line_str[2:-1]

        # La línea de código anterior separa los caracteres del principio de la lectura que "no tienen"
        # importancia en la lectura de los sensores
        # Se han identificado y separado las partes que interesan de la cadena, es decir, se intenta eliminar
        # o separar los caracteres que no se interpretan como parte de los sensore

        # Iteramos para cada uno de los valores en la cadena #
        #print(line_str)
        #variables['DO'] = -1.0  # Como no es seguro que el SW tenga este sensor, le damos un valor -1 predeterminado.
        Datos
        # Creamos el diccionario que contiene los valores de las variables #
        variables = {}

        for indx, campo in enumerate(line_str):

            if indx == 0:  # El primer campo no es un sensor, es el nombre del SW
                variables['ID'] = campo
            elif indx == 1:  # El segundo campo tampoco es un sensor, es el numero de muestra #
                variables['SAMPLE_NUM'] = campo
            else:  # El resto si son sensores
                sensor, valor = campo.split(':')  # Cada campo de line_str tiene como formato "SENSOR:VALOR"
                variables[sensor] = float(valor)  # Almacenamos el valor leido en el campo que indica el nombre sensor

        str_date = str(datetime.now())  # Leemos la fecha y la convertimos en string
        # Metemos la fecha en el diccionario de variables
        variables['DATE'] = str_date

        # creamos una tupla de parámetros que nos permitirá introducir los datos en la tabla sensor
        parametros = (variables['ID'],
                      variables['SAMPLE_NUM'],
                      variables['BAT'],
                      variables['WT'],
                      variables['PH'],
                      variables['DO'],
                      variables['COND'],
                      variables['ORP'],
                      variables['DATE'])

        # insertamos valores en nuestra tabla "sensor"
        cursor.execute("INSERT INTO sensor (ID,SAMPLE_NUM,BAT,TEMP,PH,DO,COND,ORP,DATE) VALUES(?,?,?,?,?,?,?,?,?)",
                       parametros)

        # el siguiente comando "commit()" guarda la tabla creada
        conectar.commit()
    return

#nos inventamos estos datos para que no de error la función "Basedatos"
Datos=[1, 2, 3]

while keep_going:
    #Bucle que va a leer y escribir en la base de datos los datos recibidos por los sensores y la fecha
    Basedatos(Datos)


print("Cerrando base de datos!")
conectar.close() # Cerramos la DB
print("Base de datos cerrada")
print("Cerrando puerto serie!")
ser.close() # Cerramos la com. serie
print("Puerto serie cerrado!")
exit() # Salimos del programa