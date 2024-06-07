import sqlite3
from gestorConexion import *

class pregunta():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una lista con las preguntas
#----------------------------------------------------------------------
    def listarIdPreguntaTema(self):
        self.cursor.execute("SELECT id,pregunta,idTema FROM pregunta")
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una pregunta desde un id
#----------------------------------------------------------------------
    def listarPreguntaTemaId(self,idPreguntaConsulta):
        self.cursor.execute("SELECT pregunta,respuesta1,respuesta2,respuesta3,respuesta4,correcta,idTema FROM pregunta WHERE id=(?)", (idPreguntaConsulta,))
        return self.cursor.fetchall()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una lista de preguntas de una tematica 
#----------------------------------------------------------------------
    def listarPreguntaTematica(self,idTema):
        self.cursor.execute("SELECT id,pregunta,respuesta1,respuesta2,respuesta3,respuesta4,correcta FROM pregunta WHERE idTema=(?)", (idTema,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# Crea una pregunta con pregunta 4 respuestas y tematica
#----------------------------------------------------------------------
    def crearPregunta(self,pregunta,respuesta1,respuesta2,respuesta3,respuesta4,idTema):
        self.cursor.execute("INSERT INTO pregunta VALUES(NULL,?,?,?,?,?,?,?)",(pregunta,respuesta1,respuesta2,respuesta3,respuesta4,respuesta1,idTema))
#----------------------------------------------------------------------
        
#----------------------------------------------------------------------
# Modifica una pregunta
#----------------------------------------------------------------------
    def modificarPregunta(self,pregunta,respuesta1,respuesta2,respuesta3,respuesta4,correcta,idTema,id):
        self.cursor.execute("UPDATE pregunta SET pregunta=(?),respuesta1=(?),respuesta2=(?),respuesta3=(?),respuesta4=(?),correcta=(?),idTema=(?) WHERE id=(?)",(pregunta,respuesta1,respuesta2,respuesta3,respuesta4,correcta,idTema,id))
#----------------------------------------------------------------------
