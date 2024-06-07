from datetime import datetime
import sqlite3

#----------------------------------------------------------------------
def mediaGeneral(usuario,idUsuario):
    #--      Consulta la lista de puntuaciones    --#
    arrayPuntuacionFechaTema=usuario.listarPuntuacionFechaTemaUsuario(idUsuario)
    arrayPuntuacion=[]
    lenghtPuntuacionFechaTema=len(arrayPuntuacionFechaTema)
    for x in range(0,lenghtPuntuacionFechaTema):
            arrayPuntuacion.append(arrayPuntuacionFechaTema[x][0])
    #------------------------------------------------#
    
    #--Retorna el calculo medio de las puntuaciones--#
    calculoMedia=0
    for x in range(0,len(arrayPuntuacion)):
        calculoMedia=calculoMedia+arrayPuntuacion[x]
    if len(arrayPuntuacion)==0:
        return "0%"
    return str(int((calculoMedia/len(arrayPuntuacion))*100))+"%"
    #------------------------------------------------#
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def mediaGeneralTemas(usuario,idUsuario,tematica):
    
    #--      Consulta la lista de puntuaciones    --#
    arrayPuntuacionFechaTema=usuario.listarPuntuacionFechaTemaUsuario(idUsuario)
    lenghtPuntuacionFechaTema=len(arrayPuntuacionFechaTema)
    
    arrayPuntuacion=[]
    arrayPuntuacionTemporal=[]
    
    arrayTemas=tematica.listarIdTema()
    #------------------------------------------------#
    
    #--Retorna el calculo medio de las puntuaciones--#
    for x in arrayTemas:
        arrayPuntuacionTemporal=[]
        for y in arrayPuntuacionFechaTema:
            
            temaPregunta=tematica.listarTemaPregunta(y[2])
            if temaPregunta==x[0]:
                arrayPuntuacionTemporal.append(y[0])
            
        calculoMedia=0
        for y in arrayPuntuacionTemporal:
            calculoMedia=calculoMedia+y
        if len(arrayPuntuacionTemporal)==0:
            arrayPuntuacion.append("0%")
        else:
            arrayPuntuacion.append(str(int((calculoMedia/len(arrayPuntuacionTemporal))*100))+"%")
            
    return arrayPuntuacion
    #------------------------------------------------#
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def mediaDiaTemas(usuario,idUsuario,tematica):
    
    #--      Consulta la lista de puntuaciones    --#
    arrayPuntuacionFechaTema=usuario.listarPuntuacionFechaTemaUsuario(idUsuario)
    lenghtPuntuacionFechaTema=len(arrayPuntuacionFechaTema)
    
    arrayPuntuacion=[]
    arrayPuntuacionTemporal=[]
    
    arrayTemas=tematica.listarIdTema()
    #------------------------------------------------#
    
    #--Retorna el calculo medio de las puntuaciones--#
    for x in arrayTemas:
        arrayPuntuacionTemporal=[]
        for y in arrayPuntuacionFechaTema:
            
            temaPregunta=tematica.listarTemaPregunta(y[2])
            if str(y[1])==datetime.now().strftime("%Y%m%d") and temaPregunta==x[0]:
                arrayPuntuacionTemporal.append(y[0])
            
        calculoMedia=0
        for y in arrayPuntuacionTemporal:
            calculoMedia=calculoMedia+y
        if len(arrayPuntuacionTemporal)==0:
            arrayPuntuacion.append("0%")
        else:
            arrayPuntuacion.append(str(int((calculoMedia/len(arrayPuntuacionTemporal))*100))+"%")
            
    return arrayPuntuacion
    #------------------------------------------------#
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def mediaMesTemas(usuario,idUsuario,tematica):
    
    #--      Consulta la lista de puntuaciones    --#
    arrayPuntuacionFechaTema=usuario.listarPuntuacionFechaTemaUsuario(idUsuario)
    lenghtPuntuacionFechaTema=len(arrayPuntuacionFechaTema)
    
    arrayPuntuacion=[]
    arrayPuntuacionTemporal=[]
    
    arrayTemas=tematica.listarIdTema()
    #------------------------------------------------#
    
    #--Retorna el calculo medio de las puntuaciones--#
    for x in arrayTemas:
        arrayPuntuacionTemporal=[]
        for y in arrayPuntuacionFechaTema:
            
            temaPregunta=tematica.listarTemaPregunta(y[2])
            if str(y[1])[0:6]==datetime.now().strftime("%Y%m") and temaPregunta==x[0]:
                arrayPuntuacionTemporal.append(y[0])
            
        calculoMedia=0
        for y in arrayPuntuacionTemporal:
            calculoMedia=calculoMedia+y
        if len(arrayPuntuacionTemporal)==0:
            arrayPuntuacion.append("0%")
        else:
            arrayPuntuacion.append(str(int((calculoMedia/len(arrayPuntuacionTemporal))*100))+"%")
            
    return arrayPuntuacion
    #------------------------------------------------#
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def mediaAnyoTemas(usuario,idUsuario,tematica):
    
    #--      Consulta la lista de puntuaciones    --#
    arrayPuntuacionFechaTema=usuario.listarPuntuacionFechaTemaUsuario(idUsuario)
    lenghtPuntuacionFechaTema=len(arrayPuntuacionFechaTema)
    
    arrayPuntuacion=[]
    arrayPuntuacionTemporal=[]
    
    arrayTemas=tematica.listarIdTema()
    #------------------------------------------------#
    
    #--Retorna el calculo medio de las puntuaciones--#
    for x in arrayTemas:
        arrayPuntuacionTemporal=[]
        for y in arrayPuntuacionFechaTema:
            
            temaPregunta=tematica.listarTemaPregunta(y[2])
            if str(y[1])[0:4]==datetime.now().strftime("%Y") and  temaPregunta==x[0]:
                arrayPuntuacionTemporal.append(y[0])
            
        calculoMedia=0
        for y in arrayPuntuacionTemporal:
            calculoMedia=calculoMedia+y
        if len(arrayPuntuacionTemporal)==0:
            arrayPuntuacion.append("0%")
        else:
            arrayPuntuacion.append(str(int((calculoMedia/len(arrayPuntuacionTemporal))*100))+"%")
            
    return arrayPuntuacion
    #------------------------------------------------#
#----------------------------------------------------------------------

