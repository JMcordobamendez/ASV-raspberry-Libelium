import os, sys
#import serial
import time
import sqlite3
import signal
import subprocess as sub
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
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=7)
elif puerto == "ttyUSB1":
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=7)
elif puerto == "ttyUSB2":
    ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=7)
elif puerto == "ttyUSB3":
    ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=7)
else:
    exit("The device with the SerialNumber: AH0644B8 is not connected")


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
    line = ser.readline()
    if len(line) == 0:  # mensaje no se ha recibido
        '''
        print("Time out! trying again.\n")
        '''


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
            # preguntamos a la shell por la fecha
            fecha = sub.check_output(['date +"%D/%T"'], shell=True)
            fecha=str(fecha) #formato string
            fecha=fecha.split("'")
            DATE=fecha[1]
            DATE=DATE.split("\\")
            DATE=DATE[0]

            # creamos un cursor que nos permitirá interactuar con la base de datos
            cursor = conectar.cursor()
            # creamos un vector de parámetros que nos permitirá introducir los datos en la tabla sensor
            Datos #aquí se alacenarán los datos del EMLID
            parametros = (ID, BAT, TEMP, PH, DO, COND, ORP, DATE)
            # insertamos valores en nuestra tabla "sensor"
            cursor.execute("INSERT INTO sensor (ID,BAT,TEMP,PH,DO,COND,ORP,DATE) VALUES(?,?,?,?,?,?,?,?)", parametros)
            #            print('funciona')
            #            cursor.execute("SELECT * FROM sensor WHERE ID ='SW1' ")

            # el siguiente comando "commit()" guarda la tabla creada
            conectar.commit()

            # cerramos la conexión con la base de datos
            #           conectar.close()
            #           print(cursor.fetchone())
            '''
            print(parametros)
            '''


        except:
            '''
            print('bad data!')
            '''
    return
#nos inventamos estos datos para que no de error la función "Basedatos"
Datos=[1, 2, 3]

while keep_going:
    #Bucle que va a leer y ecribir en la base de datos los datos recibidos por los sensores y la fecha
    Basedatos(Datos)


print("Cerrando base de datos!")
conectar.close() # Cerramos la DB
print("Base de datos cerrada")
print("Cerrando puerto serie!")
ser.close() # Cerramos la com. serie
print("Puerto serie cerrado!")
exit() # Salimos del programa