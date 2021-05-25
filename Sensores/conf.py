#La función de este script es que al ser ejecutado cambie la configuración de la raspberry
#sin que el usuario tenga que hacerlo de forma manual
import subprocess as sub #debido a los permisos open no puede escribir directamente en el script "99-usbserial.rules"
#Script que modifica los puertos USB para evitar el error de no distinguir entre "USB0" y "USB1"
#Cada barco tendrá uno distinto por lo que estos números de serie serán distintos
#Escribiendo en el terminal: "dmesg | grep usb" se pueden conocer los distintos números de serie de los dispositivos
ID1='"DA0071UZ"' #número de serie de la radio que usaremos con el mission planner
ID2='"AH0644B8"' #número de serie de el zigbee conectado al smart water
ID3='"JHG7GJFF"' #número de serie de el zigbee conectado al smart water ions
script1=open('text.txt','w')
script1.write("#Radio Mission Planner\n")
script1.write('ACTION=="add",ENV{ID_BUS}=="usb",ENV{ID_SERIAL_SHORT}=='+ID1+',SYMLINK+="ttyUSBPort0"\n')
script1.write("#Zigbee Smart Water\n")
script1.write('ACTION=="add",ENV{ID_BUS}=="usb",ENV{ID_SERIAL_SHORT}=='+ID2+',SYMLINK+="ttyUSBPort1"\n')
script1.write("#Zigbee Smart Water Ions\n")
script1.write('ACTION=="add",ENV{ID_BUS}=="usb",ENV{ID_SERIAL_SHORT}=='+ID3+',SYMLINK+="ttyUSBPort2"\n')
script1.close()
sub.run(["sudo cp text.txt /etc/udev/rules.d/99-usbserial.rules"],shell = True) #modifica el script de la configuración con lo escrito anteriormente
sub.run(["rm text.txt"],shell = True) #Elimina el .txt creado para poder modificar la configuración

#Script que modifija al ardurover, descomentar si se quiere usar.
#script2=open('text.txt','w') #borra lo escrito anteriormente en él
#script2.write(
#/etc/default/ardurover
# Default settings for ArduPilot for Linux.
# The file is sourced by systemd from ardurover.service

#TELEM1="-A udp:192.168.137.1:14550"
#TELEM1="-A udp:169.254.207.222:14550"
#TELEM2="-B /dev/ttyAMA0"
#TELEM3="-C /dev/ttyUSB0"
#TELEM3="-C /dev/ttyUSBPort0"
# Options to pass to ArduPilot
#ARDUPILOT_OPTS="$TELEM1 $TELEM2 $TELEM3"

                          #    # ###### #      #####
                          #    # #      #      #    #
                          ###### #####  #      #    #
                          #    # #      #      #####
                          #    # #      #      #
                          #    # ###### ###### #

# -A is a console switch (usually this is a Wi-Fi link)

# -C is a telemetry switch
# Usually this is either /dev/ttyAMA0 - UART connector on your Navio
# or /dev/ttyUSB0 if you're using a serial to USB convertor

# -B or -E is used to specify non default GPS

# Type "emlidtool ardupilot" for further help
#'''
#)
#script2.close()
#sub.run(["sudo cp text.txt /etc/default/ardurover"],shell = True) #modifica el script de la configuración con lo escrito anteriormente


