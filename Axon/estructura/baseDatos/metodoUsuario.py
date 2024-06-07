import sqlite3
from gestorConexion import *
from datetime import datetime

class usuario():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Lista todos los usuarios
#----------------------------------------------------------------------
    def listarUsuario(self):
        self.cursor.execute("SELECT nombre FROM usuario")
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una lista de puntuaciones, fecha del usuario y el tema
#----------------------------------------------------------------------
    def listarPuntuacionFechaTemaUsuario(self,idUsuario):
        self.cursor.execute("SELECT respuestaCorrecta,fecha,idPregunta FROM respuesta WHERE idUsuario=(?)", (idUsuario,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el nombre y clave con el id usuario
#----------------------------------------------------------------------
    def listarNombreClave(self,idUsuario):
        self.cursor.execute("SELECT nombre,clave FROM usuario WHERE id=(?)", (idUsuario,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el nombre con el id usuario
#----------------------------------------------------------------------
    def listarNombre(self,idUsuario):
        self.cursor.execute("SELECT nombre FROM usuario WHERE id=(?)", (idUsuario,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve la clave de un nombre de usuario
#----------------------------------------------------------------------
    def listarClave(self,nombre):
        self.cursor.execute("SELECT clave FROM usuario WHERE nombre=(?)", (nombre,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el id del usuario con el nombre
#----------------------------------------------------------------------
    def listarIdUsuarioNombre(self,nombre):
        self.cursor.execute("SELECT id FROM usuario WHERE nombre=(?)", (nombre,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Crea un usuario con nombre y clave
#----------------------------------------------------------------------
    def crearUsuario(self,nombre,clave):
        try:
            listarIdUsuarioNombre(nombre)
        except:
            self.cursor.execute("INSERT INTO usuario VALUES(NULL,?,?)", (nombre,clave))
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Crea una puntuacion con el id de usuario la tematica y puntuacion con la fecha de hoy
#----------------------------------------------------------------------
    def crearPuntuacionUsuario(self,idUsuario,idPregunta,puntuacion):
        self.cursor.execute("INSERT INTO respuesta VALUES(NULL,?,?,?,?)", (idUsuario,datetime.now().strftime("%Y%m%d"),idPregunta,puntuacion))
#----------------------------------------------------------------------
 
#----------------------------------------------------------------------
# Cambia lacalve del usuario
#----------------------------------------------------------------------
    def cambiarClaveUsuario(self,nombre,clave):
        self.cursor.execute("UPDATE usuario SET clave=(?) WHERE nombre=(?)", (clave,nombre))
#----------------------------------------------------------------------
