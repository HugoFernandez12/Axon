import sqlite3
from gestorConexion import *

class grupo():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una lista de los grupos
#----------------------------------------------------------------------
    def listarGrupos(self):
        self.cursor.execute("SELECT nombre FROM grupo")
        return self.cursor.fetchall()
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# Devuelve una lista de los usuarios y la puntuacion de un grupo
#----------------------------------------------------------------------
    def listarUsuarioPuntuacionGrupo(self,idGrupo):
        self.cursor.execute("SELECT idUsuario,puntuacion FROM usuarioGrupo WHERE idGrupo=(?)", (idGrupo,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve una lista de los grupos de un usuario
#----------------------------------------------------------------------
    def listarGruposUsuario(self,idUsuario):
        self.cursor.execute("SELECT nombre FROM grupo WHERE idUsuario=(?)", (idUsuario,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve id tema de grupo desde un id de grupo
#----------------------------------------------------------------------
    def listarIdTematicaGrupo(self,idGrupo):
        self.cursor.execute("SELECT idTema FROM grupo WHERE id = (?)", (idGrupo,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el id del grupo de nombre de grupo
#----------------------------------------------------------------------
    def listarIdGrupoNombre(self,nombre):
        self.cursor.execute("SELECT id FROM grupo WHERE nombre =(?)", (nombre,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve la puntuacion de usuario de un grupo
#----------------------------------------------------------------------
    def listarPuntuacionUsuarioGrupo(self,idUsuario,idGrupo):
        self.cursor.execute("SELECT puntuacion FROM usuarioGrupo WHERE idUsuario=(?) and idGrupo=(?)", (idUsuario,idGrupo))
        try:
            return self.cursor.fetchone()[0]
        except:
            return 0
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve la puntuacion y el id de grupo de un id de usuario
#----------------------------------------------------------------------
    def listarPuntuacionUsuarioGrupos(self,idUsuario):
        self.cursor.execute("SELECT idGrupo,puntuacion FROM usuarioGrupo WHERE idUsuario=(?)", (idUsuario,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve un id de usuario de el id de grupo
#----------------------------------------------------------------------
    def listarUsuarioGrupos(self,idGrupo):
        self.cursor.execute("SELECT idUsuario FROM usuarioGrupo WHERE idGrupo=(?)", (idGrupo,))
        return self.cursor.fetchall()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Devuelve el nombre de un id de grupo
#----------------------------------------------------------------------
    def listarNombreGrupo(self,idGrupo):
        self.cursor.execute("SELECT nombre FROM grupo WHERE id=(?)", (idGrupo,))
        return self.cursor.fetchone()[0]
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Crea un grupo con la tematica el nombre y los id de los usuarios
#----------------------------------------------------------------------
    def crearGrupo(self,idTema,nombre,arrayIdUsuario):
        self.cursor.execute("INSERT INTO grupo VALUES(NULL,?,?)", (idTema,nombre))
        for x in arrayIdUsuario:
            idGrupo=self.listarIdGrupoNombre(nombre)
            self.cursor.execute("INSERT INTO usuarioGrupo VALUES(?,?,0)",(idGrupo,x))
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Agrega una puntuacion a un usuario de grupo
#----------------------------------------------------------------------
    def agregarPuntuacionGrupo(self,idGrupo,idUsuario):
        self.cursor.execute("UPDATE usuarioGrupo SET puntuacion = puntuacion + 1 WHERE idUsuario=(?) and idGrupo=(?)", (idUsuario,idGrupo))
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# Cambia el nombre del grupo
#----------------------------------------------------------------------
    def cambiarNombreGrupo(self,nombre,nuevoNombre):
        self.cursor.execute("UPDATE grupo SET nombre = (?) WHERE nombre=(?)", (nuevoNombre,nombre))
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Borra a un usuario de un grupo
#----------------------------------------------------------------------
    def borrarUsuarioGrupo(self,idGrupo,idUsuario):
        self.cursor.execute("DELETE FROM usuarioGrupo WHERE idGrupo = (?) and idUsuario = (?)", (idGrupo,idUsuario))
#----------------------------------------------------------------------
        
#----------------------------------------------------------------------
# Borra a un grupo
#----------------------------------------------------------------------
    def borrarGrupo(self,idGrupo):
        self.cursor.execute("DELETE FROM grupo WHERE id = (?)", (idGrupo,))
#----------------------------------------------------------------------  
