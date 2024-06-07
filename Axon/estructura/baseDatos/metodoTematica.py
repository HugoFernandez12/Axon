import sqlite3
from gestorConexion import *

class tematica():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve la lista de tematicas
#----------------------------------------------------------------------
    def listarTematicas(self):
        self.cursor.execute("SELECT tematica FROM tema")
        return self.cursor.fetchall()
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# Devuelve la lista de idTema
#----------------------------------------------------------------------
    def listarIdTema(self):
        self.cursor.execute("SELECT id FROM tema")
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una tematica de grupo desde un id de grupo
#----------------------------------------------------------------------
    def listarTematicaGrupo(self,idGrupo):
        self.cursor.execute("SELECT tematica FROM tema WHERE id =(SELECT idTema FROM grupo WHERE id = (?))", (idGrupo,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve un id de tematica con el nombre del tema
#----------------------------------------------------------------------
    def listarIdTemaTematica(self,tematica):
        self.cursor.execute("SELECT id FROM tema WHERE tematica =(?)", (tematica,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve la tematica con el id
#----------------------------------------------------------------------
    def listarTematicaIdTema(self,idTematica):
        self.cursor.execute("SELECT tematica FROM tema WHERE id =(?)", (idTematica,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el tema de una pregunta
#----------------------------------------------------------------------
    def listarTemaPregunta(self,idPregunta):
        self.cursor.execute("SELECT idTema FROM pregunta WHERE id=(?)", (idPregunta,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# Agrega una nueva tematica
#----------------------------------------------------------------------
    def agregarTematica(self,nombreTematica):
        self.cursor.execute("INSERT INTO tema VALUES (NULL,(?))", (nombreTematica,))
#----------------------------------------------------------------------
