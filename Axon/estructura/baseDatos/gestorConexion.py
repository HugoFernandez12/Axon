import sqlite3

#----------------------------------------------------------------------
def conexion():
    con = sqlite3.connect("estructura/baseDatos/axon.db", check_same_thread=False)
    return con
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def cursor():
    con = conexion()
    cursor = con.cursor()
    return con,cursor
#----------------------------------------------------------------------