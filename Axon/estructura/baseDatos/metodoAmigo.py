import sqlite3
from gestorConexion import *

class amigo():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------
        
#----------------------------------------------------------------------
# Devuelve una lista de todos los amigos de una id de usuario
#----------------------------------------------------------------------
    def listarAmigos(self,idUsuario):
        self.cursor.execute("SELECT nombre FROM usuario WHERE id IN (SELECT idUsuario2 FROM amigo WHERE idUsuario1=(?))", (idUsuario,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Agrega un id de usuario a otro id de usuario
#----------------------------------------------------------------------
    def crearAmigos(self,idUsuario1,idUsuario2):
        self.cursor.execute("INSERT INTO amigo VALUES(NULL,?,?)", (idUsuario1,idUsuario2))
#----------------------------------------------------------------------