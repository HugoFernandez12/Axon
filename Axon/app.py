import threading
import sys

#----------------RECURSOS----------------------------------------------
sys.path.append("estructura")
sys.path.append("estructura/libreria")
sys.path.append("estructura/baseDatos")
sys.path.append("estructura/pregunta")
sys.path.append("estructura/media")
sys.path.append("estructura/baseDatos/creacionDDBB")
sys.path.append("estructura/baseDatos/gestorConexion")
sys.path.append("estructura/baseDatos/listarDDBB")
sys.path.append("estructura/baseDatos/metodoAmigo")
sys.path.append("estructura/baseDatos/metodoGrupo")
sys.path.append("estructura/baseDatos/metodoPregunta")
sys.path.append("estructura/baseDatos/metodoTematica")
sys.path.append("estructura/baseDatos/metodoUsuario")
sys.path.append("estructura/web")
#----------------------------------------------------------------------

#----------------WEB---------------------------------------------------
from paginaWeb import app

def webServer():
    app.run()
    
if __name__=="__main__":
    webServerThread=threading.Thread(target=webServer)
    webServerThread.start()
#----------------------------------------------------------------------