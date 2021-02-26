#importar librería de sqlite
import sqlite3

#nos conectamos con la base de datos llamada prueba1.db
#si no existe crea una con ese nombre en el mismo directorio
conectar=sqlite3.connect("prueba1.db")

#Creamos un cursor que nos permitirá interactuar con la base de datos
cursor=conectar.cursor()

#ahora creamos la tabla con los datos que guardaremos
cursor.execute("""CREATE TABLE sensor(
                ID text,
                BAT real,
                TEMP real,
                PH real,
                DO real,
                COND real,
                ORP real
                )""")

#el siguiente comando "commit()" guarda la tabla creada
conectar.commit()

#cerramos la conexión con la base de datos
conectar.close()