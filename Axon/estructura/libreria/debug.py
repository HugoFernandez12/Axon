import socket
import select
import time
from buffer import *
from datetime import datetime
import threading
import os.path

lock = threading.RLock()
b=buffer(20000)
class logger():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,puerto,depuracion,dias):
        self.puerto=puerto
        self.depuracion=depuracion
        self.dias=dias
        self.conexion=""
        self.iniciarServidor()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Abre el socket como servidor para que el cliente pueda conectarse
#----------------------------------------------------------------------
    def enviarSocket(self):
        HOST = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, self.puerto))
        s.listen()
        while True:
            listaSockets = [s]
            ready_to_read, ready_to_write, in_error = select.select(listaSockets, listaSockets, [], 0.1)
            if len(ready_to_read) != 0:
                for sock in ready_to_read:
                    if sock is s:
                        conn, addr = s.accept()
                        print("addr ",addr)
                        socketRead = [conn]
                        print(f"Connected by {addr}")
                        self.conexion=conn
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Envia,guarda y muestra el log por distintos origenes. Filtra por nivel de depuracion
#----------------------------------------------------------------------
    def mensaje(self,nivel,texto):
        with lock: 
            d=datetime.now().strftime("%Y%m%d %H%M%S.%f")[:-3]
#------------------SOCKET----------------------------------------------
            if int(nivel)<=int(self.depuracion):
                if type(self.conexion) is socket.socket:
                    try:
                        self.conexion.sendall(b.crearTrama(d+" "+nivel+" "+texto).encode())
                    except:
                        self.conexion.close()
                        self.conexion=""
#----------------------------------------------------------------------
#------------------FICHERO---------------------------------------------
                ruta="estructura/libreria/logs/logs_"+str(datetime.now().strftime("%Y%m%d"))+".log"
                if os.path.isfile(ruta):
                    f = open(ruta, "a")
                    f.write(d+" "+nivel+" "+texto+"\n")
                    self.borradoFichero()
                else:
                    open(ruta, "x")
                    f = open(ruta, "a")
                    f.write(d+" "+nivel+" "+texto+"\n")
                    self.borradoFichero()
#----------------------------------------------------------------------
            
#------------------CONSOLA---------------------------------------------
                print(d+" "+nivel+" "+texto)
#----------------------------------------------------------------------
#----------------------------------------------------------------------    

#----------------------------------------------------------------------
    def fatal(self,texto):
        self.mensaje("1",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def critical(self,texto):
        self.mensaje("2",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def error(self,texto):
        self.mensaje("3",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def warning(self,texto):
        self.mensaje("4",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def notice(self,texto):
        self.mensaje("5",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def information(self,texto):
        self.mensaje("6",texto)
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
    def trace(self,texto):
        self.mensaje("7",texto)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Calcula si el anyo es bisiesto
#----------------------------------------------------------------------
    def anyoBisiesto(self):
        if int(datetime.now().year) % 4 == 0:
            if int(datetime.now().year) % 100 == 0:
                if int(datetime.now().year) % 400 == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Borra el log que tenga una antiguedad, varia en el constructor
#----------------------------------------------------------------------
    def fechaBorrado(self):
        control=int(datetime.now().day)-self.dias
            #COMPRUEBAS QUE NO SEA MENOR QUE 0
        if control<=0:
            #CALCULAS LOS DIAS QUE DEBES RESTAR
            if control==0:
                diasRestar=0
            else:
                for x in range(1,32):
                    if(control+x==0):
                        diasRestar=x
                        break
            #CALCULAS CUANTOS DIAS DEBES RESTAR DEPENDE DEL MES
            mesComprobar=int(datetime.now().month)-1
            #COMPRUEBAS LOS DIAS DEL MES
            if mesComprobar==0:
                mesComprobar=12
            if int(mesComprobar)==1 or int(mesComprobar)==3 or int(mesComprobar)==5 or int(mesComprobar)==7 or int(mesComprobar)==8 or int(mesComprobar)==10 or int(mesComprobar)==12:
                diasRestar=31-diasRestar   
            elif int(mesComprobar)==4 or int(mesComprobar)==6 or int(mesComprobar)==9 or int(mesComprobar)==11:
                diasRestar=30-diasRestar
            elif int(mesComprobar)==2:
                #SI ES BISIESTO RESTAS 1 MAS
                if self.anyoBisiesto():
                    diasRestar=29-diasRestar
                else:
                    diasRestar=28-diasRestar
            #GUARDAS EL MES Y LOS DIAS
            controlMes=int(datetime.now().strftime("%m"))-1
            dias=str(diasRestar)
            #SI ES CERO BAJAS 1 ANYO
            if controlMes==0:
                controlAnyo=int(datetime.now().strftime("%Y"))-1
                fechaBorrar=str(controlAnyo)+"12"+dias
                return fechaBorrar

            else:
                if len(str(controlMes))==1:
                    controlMes="0"+str(controlMes)
                fechaBorrar=str(datetime.now().strftime("%Y"))+str(controlMes)+dias
                return fechaBorrar
                
        else:
            #CONSIGUES LA FECHA A COMPROBAR
            if len(str(control))==1:
                control="0"+str(control)
            fechaBorrar=str(datetime.now().strftime("%Y%m"))+str(control)
            return fechaBorrar
#----------------------------------------------------------------------

#----------------------------------------------------------------------
    def borradoFichero(self):
        
        carpeta="estructura/libreria/logs"
        
        y=self.fechaBorrado()
        for x in os.listdir(carpeta):
            rutaAr=os.path.join(carpeta, x)
            if os.path.isfile(rutaAr):
                fechaMod=os.path.getctime(rutaAr)
                fechaMod=datetime.fromtimestamp(fechaMod)
                fechaMod=fechaMod.strftime("%Y%m%d")
                if y>fechaMod:
                    if os.path.isfile(rutaAr):
                        os.remove(rutaAr)
                if int(y)>int(x[5:13]):
                    if os.path.isfile(rutaAr):
                        os.remove(rutaAr)
#----------------------------------------------------------------------
                        
#----------------------------------------------------------------------
# Inicial un hilo para que el socket este abierto y envie mensajes
#----------------------------------------------------------------------
    def iniciarServidor(self):
        threading.Thread(target=self.enviarSocket).start()
#----------------------------------------------------------------------