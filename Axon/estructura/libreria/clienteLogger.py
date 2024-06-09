import socket
import select
from buffer import *

#----------------------------------------------------------------------
# Cliente que se conecta con el log para verlo por TCP
#----------------------------------------------------------------------
b=buffer(20000)
HOST = "127.0.0.1"
PORT = 22999
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    socketRead = [s]
    while True:
        try:
            readyRead,_,_=select.select(socketRead,[],[],0.1)
        except:
            s.close()
            
        for ready in readyRead:
            if ready==s:
                data = ready.recv(10000)
                if data:
                    data = data.decode()
                    b.añadirTrama(data)
                    while(data!=""):
                        data = b.extraerTrama()
                        if(data!=""):
                            print(data)
#----------------------------------------------------------------------