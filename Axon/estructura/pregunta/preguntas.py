import random
from metodoPregunta import *
from metodoTematica import *


#----------------------------------------------------------------------
def preguntaAleatoria(tematica,pregunta):
    #--Calcula el id de la tematica aleatoriamente --#
    x=tematica.listarTematicas()
    
    idTematica=int(random.random()*len(x)+1)
    #------------------------------------------------#
    
    #-- Retorna la pregunta con las respuestas en  --#
    #-- posicion aleatoria controlando la correcta --#
    arrayPreguntas=pregunta.listarPreguntaTematica(idTematica)
    while len(arrayPreguntas)==0:
        idTematica=int(random.random()*len(x)+1)
        arrayPreguntas=pregunta.listarPreguntaTematica(idTematica)
        
    preguntaRandom=int(random.random()*len(arrayPreguntas))
    idPregunta,pregunta,res1,res2,res3,res4,correcta=arrayPreguntas[preguntaRandom]
    respuestasRandom=[res1,res2,res3,res4]
    random.shuffle(respuestasRandom)
    res1,res2,res3,res4=respuestasRandom
    
    return idPregunta,pregunta,res1,res2,res3,res4,correcta,tematica.listarTematicaIdTema(idTematica)
    #------------------------------------------------#
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def preguntaAleatoriaGrupo(idGrupo,tematica,pregunta,grupo):
    #--Calcula el id de la tematica aleatoriamente --#
    idTematica=grupo.listarIdTematicaGrupo(idGrupo)
    #------------------------------------------------#
    
    #-- Retorna la pregunta con las respuestas en  --#
    #-- posicion aleatoria controlando la correcta --#
    if idTematica==2:
        return matematicas()
    else:
        arrayPreguntas=pregunta.listarPreguntaTematica(idTematica)
        preguntaRandom=int(random.random()*len(arrayPreguntas))
        idPregunta,pregunta,res1,res2,res3,res4,correcta=arrayPreguntas[preguntaRandom]
        respuestasRandom=[res1,res2,res3,res4]
        random.shuffle(respuestasRandom)
        res1,res2,res3,res4=respuestasRandom
        
        return pregunta,res1,res2,res3,res4,correcta,tematica.listarTematicaIdTema(idTematica)
    #------------------------------------------------#
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
def matematicas():
    #--Calcula aleatoriamente el tipo de pregunta --#
    tipo=int(random.random()*3)
    #------------------------------------------------#
    
    #-- Retorna la pregunta con las respuestas en  --#
    #-- posicion aleatoria controlando la correcta --#
    if tipo==0:

        y=int(random.random()*4)
        arrayRespuesta=["0","0","0","0"]
        for x in range(0,4):
            mult1=int(random.random()*8+2)
            mult2=int(random.random()*998+2)
            arrayRespuesta[x]=str(mult1*mult2)
            if x==y:
                correcta=str(arrayRespuesta[x])
                pregunta=str(mult1)+" * "+str(mult2)
        
    elif tipo==1:
        
        y=int(random.random()*4)
        arrayRespuesta=["0","0","0","0"]
        for x in range(0,4):
            suma1=int(random.random()*1000+9000)
            suma2=int(random.random()*1000)
            resta=int(random.random()*5000)
            arrayRespuesta[x]=str(suma1+suma2-resta)
            if x==y:
                correcta=str(arrayRespuesta[x])
                pregunta=str(suma1)+" + "+str(suma2)+" - "+str(resta)
    
    elif tipo==2:
        
        y=int(random.random()*4)
        arrayRespuesta=["0","0","0","0"]
        for x in range(0,4):
            divid=int(random.random()*998+2)
            divis=int(random.random()*8+2)
            arrayRespuesta[x]=str(int(divid/divis))
            if x==y:
                correcta=str(arrayRespuesta[x])
                pregunta=str(divid)+"/"+str(divis)

    return pregunta,correcta,arrayRespuesta[0],arrayRespuesta[1],arrayRespuesta[2],arrayRespuesta[3],"Matematicas"
    #------------------------------------------------#
#----------------------------------------------------------------------