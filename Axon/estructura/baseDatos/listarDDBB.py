import sqlite3
from gestorConexion import *


class listar():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# lista la base de datos
#----------------------------------------------------------------------
    def listarDDBB(self):
        print("----tema----")
        self.cursor.execute("SELECT * FROM tema")
        for row in self.cursor.fetchall():
            print(row)

        print("----usuario----")
        self.cursor.execute("SELECT * FROM usuario")
        for row in self.cursor.fetchall():
            print(row)

        print("----respuesta----")
        self.cursor.execute("SELECT * FROM respuesta")
        for row in self.cursor.fetchall():
            print(row)

        print("----amigo----")
        self.cursor.execute("SELECT * FROM amigo")
        for row in self.cursor.fetchall():
            print(row)
            
        print("----grupo----")
        self.cursor.execute("SELECT * FROM grupo")
        for row in self.cursor.fetchall():
            print(row)
            
        print("----usuarioGrupo----")
        self.cursor.execute("SELECT * FROM usuarioGrupo")
        for row in self.cursor.fetchall():
            print(row)

        print("----pregunta----")
        self.cursor.execute("SELECT * FROM pregunta")
        for row in self.cursor.fetchall():
            print(row)
#----------------------------------------------------------------------
