import os, sys
import serial
import time
import sqlite3
import multiprocessing
#Crea un objeto serie con la dirección, baudrate, tiempo de espera (este último se modifica de 5 a 7 para que de tiempo de lectura y no retorne line en blanco o erro de lectura)
ser = serial.Serial('/dev/ttyUSB0',115200, timeout = 7)

#nos conectamos con la base de datos llamada prueba1.db
conectar=sqlite3.connect("prueba1.db")

#creamos un cursor que nos permitirá interactuar con la base de datos
cursor=conectar.cursor()
def Basedatos (Datos):
    line = ser.readline()
    if len(line) == 0:  # mensaje no se ha recibido
        print("Time out! trying again.\n")

    else:
        #    continue
        # Requiere que los datos sean de tipo string para guardarlos en txt
        line_str = str(line)
        line_str = line_str.split('#')
        # La línea de código anterior separa los caracteres del principio de la lectura que "no tienen" importancia en la lectura de los sensores
        # Se han identificado y separado las partes que interesan de la cadena, es decir se intenta eliminar o separar los caracteres que no se interpretan como parte de los sensores
        try:
            ID = line_str[2]  # nombre del dispositivo “SW1” por ejemplo
            SAMPLE_NUM = line_str[3]  # número de muestras al que corresponde cada lectura de los sensores
            # Batería
            BATdata = line_str[4]  # Nivel de batería
            BATdata = BATdata.split(':')  # quiero quedarme con el número
            BAT = int(BATdata[1])
            # sensor temperatura
            TEMPdata = line_str[5]  # temperatura
            TEMPdata = TEMPdata.split(':')  # quiero quedarme con el número
            TEMP = float(TEMPdata[1])
            # sensor pH
            PHdata = line_str[6]  # pH
            PHdata = PHdata.split(':')  # quiero quedarme con el número
            PH = float(PHdata[1])
            # sensor O2
            DOdata = line_str[7]  # %O2
            DOdata = DOdata.split(':')  # quiero quedarme con el número
            DO = float(DOdata[1])
            # sensor COND
            CONDdata = line_str[8]
            CONDdata = CONDdata.split(':')
            COND = float(CONDdata[1])
            # sensor ORP
            ORPdata = line_str[9]  # ORP
            ORPdata = ORPdata.split(':')
            ORP = float(ORPdata[1])
            # creamos un cursor que nos permitirá interactuar con la base de datos
            cursor = conectar.cursor()
            # creamos un vector de parámetros que nos permitirá introducir los datos en la tabla sensor
            Datos #aquí se alacenarán los datos del EMLID
            parametros = (ID, BAT, TEMP, PH, DO, COND, ORP)
            # insertamos valores en nuestra tabla "sensor"
            cursor.execute("INSERT INTO sensor (ID,BAT,TEMP,PH,DO,COND,ORP) VALUES(?,?,?,?,?,?,?)", parametros)
            #            print('funciona')
            #            cursor.execute("SELECT * FROM sensor WHERE ID ='SW1' ")

            # el siguiente comando "commit()" guarda la tabla creada
            conectar.commit()

            # cerramos la conexión con la base de datos
            #           conectar.close()
            #           print(cursor.fetchone())
            print(parametros)


        except:
            print('bad data!')
    return


Datos=[1, 2, 3]
p1 = multiprocessing.Process(target=Basedatos, args=(Datos,))# inicializamos el multiprocesador, si no da error el if

while True:
    if p1.is_alive() == False: #De esta forma solo se lanza un proceso en paralelo cada vez
        # inicializamos el multiprocesador
        p1 = multiprocessing.Process(target=Basedatos, args=(Datos,))
        p1.start()
#    else:
        