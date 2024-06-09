from flask import render_template, request, Flask, redirect, url_for, Response, send_from_directory
import sys

#----------------LOG---------------------------------------------------
from libreria.debug import *
log=logger(22999,10,7)
#----------------------------------------------------------------------

#----------------DDBB--------------------------------------------------
from media.medias import *
from pregunta.preguntas import *
from creacionDDBB import *
from gestorConexion import *
from listarDDBB import *
from metodoAmigo import *
from metodoGrupo import *
from metodoPregunta import *
from metodoTematica import *
from metodoUsuario import *
#----------------------------------------------------------------------

#----------------RECURSOS----------------------------------------------
conexion,cursor=cursor()

creacionDDBB=creacionDDBB(conexion,cursor)
listar=listar(conexion,cursor)
tematica=tematica(conexion,cursor)
amigo=amigo(conexion,cursor)
grupo=grupo(conexion,cursor)
pregunta=pregunta(conexion,cursor)
usuario=usuario(conexion,cursor)
#----------------------------------------------------------------------

#----------------CREACION/LISTADO-DDBB---------------------------------
# creacionDDBB.crearDDBB()
# creacionDDBB.cargarDDBB()
# listar.listarDDBB()
# conexion.commit()
#----------------------------------------------------------------------

#----------------VARIABLES---------------------------------------------
usuarioConectado=""
cont=0
arrayCorrectasUsuario=[0,0,0,0,0]
tmp=""
error=""
arrayAmigoGrupo=[]
lenghtAmigosGrupo=0
nombreGrupo=""
grupoJugar=0
grupoAdministrar=0
mensajeControl=""
usuarioPerfil=""
idPreguntaConsulta=0
controlFiltroTema=0
arrayIdPregunta=[]
arrayPregunta=[]
temaGrupo=""
temaFiltro=""
controlModificacionPregunta=True
arrayControlUsuarios=[]
lenghtArrayControlUsuarios=0
#----------------------------------------------------------------------

#----------------FLASK-------------------------------------------------
app = Flask(__name__)
#----------------------------------------------------------------------

#----------------MENU-PRINCIPAL----------------------------------------
@app.route('/principal',methods=['GET', 'POST'])
def principal():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    return render_template('axon.html')
#----------------------------------------------------------------------

#----------------PERFIL-PERSONAL---------------------------------------
@app.route('/perfil',methods=['GET', 'POST'])
def perfil():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado
    if usuarioConectado=="":
        return redirect("/")
    log.information("El usuario "+usuarioConectado+" esta consutando su perfil.")
    #------------------------------------------------#
    
    data = request.form
    media="Dia"
    
    #--Consulta el id del usuario con el nombre del--#
    #--        usuario conectado actualmente       --#
    idUsuario=usuario.listarIdUsuarioNombre(usuarioConectado)
    #------------------------------------------------#
    
    #--   Consulta las medias del usuario actual   --#
    mediaUsuarioGeneral=mediaGeneral(usuario,idUsuario)
    
    arrayTemas=tematica.listarTematicas()
    lenghtArrayTemas=len(arrayTemas)
    
    arrayMediaDia=mediaDiaTemas(usuario,idUsuario,tematica)
    
    arrayMediaMes=mediaMesTemas(usuario,idUsuario,tematica)
    
    arrayMediaAnyo=mediaAnyoTemas(usuario,idUsuario,tematica)
    
    arrayMediaGeneral=mediaGeneralTemas(usuario,idUsuario,tematica)

    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #-- redirigirte a otra pagina o consultar una  --#
    #--                   media                    --#
    if(len(data)!=0):
        if request.form.get("amigo") == "Amigos":
            log.information("El usuario "+usuarioConectado+" ha entrado al gestor de amigos.")
            return redirect("/amigos")
        if request.form.get("grupo") == "Grupos":
            log.information("El usuario "+usuarioConectado+" ha entrado a la gestion de grupos.")
            return redirect("/grupo")
        if request.form.get("clave") == "Cambiar Clave":
            log.information("El usuario "+usuarioConectado+" ha entrado a la gestion de su clave.")
            return redirect("/cambiarClave")
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El usuario "+usuarioConectado+" ha cerrado sesion.")
            return redirect("/")
        
        media=request.form.get("media")
    #------------------------------------------------#
        
    return render_template('axon2.html',usuarioConectado=usuarioConectado,media=media,arrayTemas=arrayTemas,lenghtArrayTemas=lenghtArrayTemas,
                           mediaUsuarioGeneral=mediaUsuarioGeneral,arrayMediaDia=arrayMediaDia,arrayMediaMes=arrayMediaMes,
                           arrayMediaAnyo=arrayMediaAnyo,arrayMediaGeneral=arrayMediaGeneral)
#----------------------------------------------------------------------

#----------------AMIGOS------------------------------------------------
@app.route('/amigos',methods=['GET', 'POST'])
def amigos():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    error=""
    data = request.form
    
    #--Consulta el id del usuario con el nombre del--#
    #--  usuario conectado actualmente.Consulta la --#
    #--  lista de amigos y la guarda en un array   --#
    idUsuario=usuario.listarIdUsuarioNombre(usuarioConectado)
    arrayAmigos=amigo.listarAmigos(idUsuario)
    lenghtAmigos=len(arrayAmigos)
    #------------------------------------------------#
        
    #--   Recoge la informacion de la web para     --#
    #--            agregar un amigo                --#
    if(len(data)!=0):
        if request.form.get("aregarAmigo")=="Agregar":
            nombreAmigo = request.form.get("textoAgregarAmigo")
            if nombreAmigo!="":
                try:
                    idAmigo=usuario.listarIdUsuarioNombre(nombreAmigo)
                    amigo.crearAmigos(idUsuario,idAmigo)
                    conexion.commit()
                    log.information("El usuario "+usuarioConectado+" ha agregado un nuevo amigo.")
                    return redirect("/amigos")
                except:
                    error="No se encontro a "+nombreAmigo+" o ya esta agregado."
                    log.error("ERROR: No se encontro a "+nombreAmigo+" o ya esta agregado.")
            else:
                error="El nombre no puede estar vacio"
                log.error("ERROR: Nombre de amigo vacio.")
    #------------------------------------------------#
                
    
    #--  Guarda en un array la puntuacion de los   --#
    #--                amigos                      --#
    arrayPuntuacionAmigos=[]
    for x in arrayAmigos:
        arrayPuntuacionAmigos.append(mediaGeneral(usuario,usuario.listarIdUsuarioNombre(x[0])))
    #------------------------------------------------#
    
    return render_template('axon3.html',arrayAmigos=arrayAmigos,error=error,lenghtAmigos=lenghtAmigos,arrayPuntuacionAmigos=arrayPuntuacionAmigos)
#----------------------------------------------------------------------

#----------------JUEGO-1-JUGADOR---------------------------------------
@app.route('/axon',methods=['GET', 'POST'])
def axon():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global cont,tmp,usuarioConectado,arrayCorrectasUsuario
    lenghtArrayCorrectasUsuario=len(arrayCorrectasUsuario)
    if usuarioConectado=="":
        return redirect("/")
    log.information("El usuario "+usuarioConectado+" esta jugando.")
    #------------------------------------------------#
    
    #-- Recibe una pregunta aleatoria de tematica  --#
    #--                  aleatoria                 --#
    idPregunta,preguntaWeb,respuesta1,respuesta2,respuesta3,respuesta4,correcta,tema=preguntaAleatoria(tematica,pregunta)
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #-- comprobar si la respuesta es correcta o no --#
    data = request.form
    if(len(data)!=0):
        if request.form.get("respuesta1")==tmp or request.form.get("respuesta2")==tmp or request.form.get("respuesta3")==tmp or request.form.get("respuesta4")==tmp:
            usuario.crearPuntuacionUsuario(usuario.listarIdUsuarioNombre(usuarioConectado),idPregunta,1)
            conexion.commit()
            log.information("El usuario "+usuarioConectado+" ha acertado la pregunta.")
            arrayCorrectasUsuario[cont]=1
            cont=cont+1
        elif request.form.get("play"):
            pass
        else:
            usuario.crearPuntuacionUsuario(usuario.listarIdUsuarioNombre(usuarioConectado),idPregunta,0)
            conexion.commit()
            log.information("El usuario "+usuarioConectado+" ha fallado la pregunta")
            cont=cont+1
    tmp=correcta
    #------------------------------------------------#
    
    return render_template('axon4.html',tema=tema,preguntaWeb=preguntaWeb,correcta=correcta,respuesta1=respuesta1
                           ,respuesta2=respuesta2,respuesta3=respuesta3,respuesta4=respuesta4,arrayCorrectasUsuario=arrayCorrectasUsuario,cont=cont,lenghtArrayCorrectasUsuario=lenghtArrayCorrectasUsuario)
#----------------------------------------------------------------------

#----------------JUEGO-EN-GRUPO----------------------------------------
@app.route('/axonGrupo',methods=['GET', 'POST'])
def axonGrupo():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global tmp,usuarioConectado
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    #--Consulta el nombre del grupo elegido y elige--#
    #--una pregunta aleatoria con el tema del grupo--#
    nombreGrupo=grupo.listarNombreGrupo(grupoJugar)
    log.information("El usuario "+usuarioConectado+" esta jugando en el grupo "+nombreGrupo+".")
    preguntaWeb,respuesta1,respuesta2,respuesta3,respuesta4,correcta,tema=preguntaAleatoriaGrupo(grupoJugar,tematica,pregunta,grupo)
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #-- comprobar si la respuesta es correcta o no --#
    data = request.form
    if(len(data)!=0):
        if request.form.get("respuesta1")==tmp or request.form.get("respuesta2")==tmp or request.form.get("respuesta3")==tmp or request.form.get("respuesta4")==tmp:
            grupo.agregarPuntuacionGrupo(grupoJugar,usuario.listarIdUsuarioNombre(usuarioConectado))
            conexion.commit()
            log.information("El usuario "+usuarioConectado+" ha acertado la pregunta en el grupo "+nombreGrupo+".")
    tmp=correcta
    #------------------------------------------------#
            
    return render_template('axon5.html',preguntaWeb=preguntaWeb,correcta=correcta,respuesta1=respuesta1
                           ,respuesta2=respuesta2,respuesta3=respuesta3,respuesta4=respuesta4,nombreGrupo=nombreGrupo)
#----------------------------------------------------------------------

#----------------LOGIN/REGISTER----------------------------------------
@app.route('/',methods=['GET', 'POST'])
def index():
    
    #-- Desconecta al usuario conectado si hay uno --#
    global error,usuarioConectado,cont,arrayCorrectasUsuario
    cont=0
    usuarioConectado=""
    error=""
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #-- comprobar si se quiere registrar o iniciar --#
    #--sesion y comprueba que los datos esten bien --#
    #--si el usuario es administrador lo lleva a la--#
    #--      pagina de creacion de preguntas       --#
    data = request.form
    if(len(data)!=0):
        nombre = request.form.get("nombre")
        nombre =nombre.strip()
        clave = request.form.get("clave")
        clave=clave.strip()
        login = request.form.get("login")
        register = request.form.get("register")
        if login=="login":
            
            if nombre=="admin" and clave=="admin":
                usuarioConectado=nombre
                log.information("El usuario "+usuarioConectado+" ha iniciado sesion.")
                log.information("El usuario "+usuarioConectado+" ha entrado al gestor de preguntas.")
                arrayCorrectasUsuario=[0,0,0,0,0]
                return redirect("/grupoAdmin")
            
            try:
                idUsuario=usuario.listarIdUsuarioNombre(nombre)
                claveUsuario=usuario.listarClave(nombre)
                if clave==claveUsuario:
                    usuarioConectado=nombre
                    log.information("El usuario "+usuarioConectado+" ha iniciado sesion.")
                    log.information("El usuario "+usuarioConectado+" ha entrado al menu principal.")
                    return redirect("/principal")
                else:
                    error="ERROR en la clave"
                    log.error("ERROR: No se encontro la clave.")
            except:
                error="ERROR en el usuario"
                log.error("ERROR: No se encontro el usuario.")

        elif register=="register":
            
            try:
                idUsuario=usuario.listarIdUsuarioNombre(nombre)
                error="Ya esiste ese usuario"
                log.error("ERROR: El usuario ya existe.")
            except:
                if nombre!="" and clave!="":
                    usuario.crearUsuario(nombre,clave)
                    conexion.commit()
                    usuarioConectado=nombre
                    log.information("El usuario "+usuarioConectado+" se ha registrado en Axon.")
                    log.information("El usuario "+usuarioConectado+" ha entrado al menu principal.")
                    return redirect("/principal")
                else:
                    error="El usuario o la clave no pueden estar vacios"
                    log.error("ERROR: El usuario o la clave no pueden estar vacios.")
    #------------------------------------------------#
        
    return render_template('axon6.html',error=error)
#----------------------------------------------------------------------

#----------------GRUPOS-DEL-USUARIO------------------------------------
@app.route('/grupo',methods=['GET', 'POST'])
def listaGrupo():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,grupoJugar,arrayAmigoGrupo
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    
    #--Guarda en dos arrays el nombre de lod grupos--#
    #--  del usuario y su puntuacion en cada uno   --#
    idUsuario=usuario.listarIdUsuarioNombre(usuarioConectado)
    
    arrayGrupo=[]
    arrayPuntuacion=[]
    
    arrayGrupoPuntuacion=grupo.listarPuntuacionUsuarioGrupos(idUsuario)
    lenghtGrupoPuntuacion=len(arrayGrupoPuntuacion)
    for x in range(0,lenghtGrupoPuntuacion):
        arrayGrupo.append(grupo.listarNombreGrupo(arrayGrupoPuntuacion[x][0]))
        arrayPuntuacion.append(arrayGrupoPuntuacion[x][1])
    #------------------------------------------------#
    
    #-- Recoge la informacion de la web para ir a  --#
    #--crear un grupo o jugar con el grupo elegido --#
    data = request.form
    if(len(data)!=0):
        if request.form.get("crearGrupo") == "Crear Grupo":
            log.information("El usuario "+usuarioConectado+" ha entrado a la creacion de grupos.")
            arrayControlUsuarios.clear()
            arrayAmigoGrupo.clear()
            return redirect("/crearGrupo")
    
        for x in range(0,lenghtGrupoPuntuacion):
            if "Jugar" == request.form.get(str(x)):
                grupoJugar=arrayGrupoPuntuacion[x][0]
                return redirect("/axonGrupo")
            
        for x in range(0,lenghtGrupoPuntuacion):
            if "Ver Grupo" == request.form.get(str(x)):
                grupoJugar=arrayGrupoPuntuacion[x][0]
                return redirect("/puntuacionesGrupo")
            
        for x in range(0,lenghtGrupoPuntuacion):
            if "Salir del Grupo" == request.form.get(str(x)):
                idGrupoBorrar=arrayGrupoPuntuacion[x][0]
                grupo.borrarUsuarioGrupo(idGrupoBorrar,idUsuario)
                conexion.commit()
                return redirect("/grupo")
    #------------------------------------------------#
        
    return render_template('axon7.html',arrayGrupo=arrayGrupo,arrayPuntuacion=arrayPuntuacion,lenghtGrupoPuntuacion=lenghtGrupoPuntuacion)
#----------------------------------------------------------------------

#----------------CREACION-DE-GRUPOS------------------------------------
@app.route('/crearGrupo',methods=['GET', 'POST'])
def crearGrupo():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,arrayAmigoGrupo,lenghtAmigosGrupo,error,nombreGrupo,mensajeControl,temaGrupo,arrayControlUsuarios,lenghtArrayControlUsuarios
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    mensajeControl=""
    error=""
    control=True
    controlGrupoExiste=False
    controlUsuarioGrupo=False
        
           
    #--   Guarda en un array la lista de amigos    --#
    idUsuario=usuario.listarIdUsuarioNombre(usuarioConectado)
    arrayAmigos=amigo.listarAmigos(idUsuario)
    lenghtAmigos=len(arrayAmigos)
    arrayTemas=tematica.listarTematicas()
    #------------------------------------------------#
    
    
    if len(arrayControlUsuarios)==0:
        for x in range(0,lenghtAmigos):
            arrayControlUsuarios.append(0)
        lenghtArrayControlUsuarios=len(arrayControlUsuarios)
        
    
    #--   Recoge la informacion de la web para     --#
    #--elegir el tema,los usuarios y crear un grupo--#
    data = request.form
    if(len(data)!=0):
        nombreGrupo=request.form.get("nombreGrupo")
        nombreGrupo=nombreGrupo.strip()
        for x in range(0,lenghtAmigos):
            if "Agregar" == request.form.get(str(x)):
                arrayControlUsuarios[x]=1
                temaGrupo = request.form.get("tema")
                for y in range(0,lenghtAmigosGrupo):
                    if arrayAmigos[x] == arrayAmigoGrupo[y]:
                        control=False
                        break
                if control:
                    arrayAmigoGrupo.append(arrayAmigos[x])
                    lenghtAmigosGrupo=len(arrayAmigoGrupo)
                else:
                    break
                
        if request.form.get("borrarAmigosGrupo")=="Borrar":
            arrayControlUsuarios.clear()
            for x in range(0,lenghtAmigos):
                arrayControlUsuarios.append(0)
            lenghtArrayControlUsuarios=len(arrayControlUsuarios)
            temaGrupo = request.form.get("tema")
            arrayAmigoGrupo.clear()
            lenghtAmigosGrupo=len(arrayAmigoGrupo)
            
            
        if request.form.get("crearGrupo")=="Crear":
            try:
                temaGrupo = request.form.get("tema")
                idTema=tematica.listarIdTemaTematica(temaGrupo)
                arrayIdUsuario=[]
                for x in range(0,lenghtAmigosGrupo):
                    y=usuario.listarIdUsuarioNombre(arrayAmigoGrupo[x][0])
                    arrayIdUsuario.append(y)
                if len(arrayIdUsuario)!=0:
                    controlUsuarioGrupo=True
                    arrayIdUsuario.append(idUsuario)
                    
                for x in range(0,len(grupo.listarGrupos())):
                    if grupo.listarGrupos()[x][0]==nombreGrupo:
                        controlGrupoExiste=True
                        break
                    
                if controlGrupoExiste==False:
                    if controlUsuarioGrupo:
                        if nombreGrupo!="":
                            grupo.crearGrupo(idTema,nombreGrupo,arrayIdUsuario)
                            conexion.commit()
                            mensajeControl="Has creado un nuevo grupo con exito"
                            log.information("El usuario "+usuarioConectado+" ha creado el grupo "+nombreGrupo+".")
                            nombreGrupo=""
                        else:
                            error="El nombre del grupo no puede estar vacio"
                            log.error("ERROR: El nombre del grupo no puede estar vacio.")
                    else:
                        error="No se ha agreagado ningun usuario al grupo "+nombreGrupo
                        log.error("ERROR: No se han asignado usuarios al grupo.")
                else:
                    error="El grupo ya existe"
                    log.error("ERROR: No se pudo crear el grupo.")
            except:
                error="Error al crear el grupo"
                log.error("ERROR: No se pudo crear el grupo.")
    #------------------------------------------------#
                
    return render_template('axon8.html',mensajeControl=mensajeControl,nombreGrupo=nombreGrupo,error=error,
                           arrayAmigos=arrayAmigos,lenghtAmigos=lenghtAmigos,arrayAmigoGrupo=arrayAmigoGrupo,
                           lenghtAmigosGrupo=lenghtAmigosGrupo,arrayTemas=arrayTemas,temaGrupo=temaGrupo,arrayControlUsuarios=arrayControlUsuarios)
#----------------------------------------------------------------------


#----------------CREACION-DE-PREGUNTAS----------------------------------
@app.route('/crearPreguntasAdmin',methods=['GET', 'POST'])
def crearPreguntasAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,mensajeControl
    if usuarioConectado!="admin":
        return redirect("/")
    error=""
    mensajeControl=""
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #--   crear una pregunta con sus respuestas    --#
    arrayTemas=tematica.listarTematicas()
    data = request.form
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        if request.form.get("crearPregunta")=="Crear pregunta":
            preguntaWeb = request.form.get("pregunta")
            respuesta1 = request.form.get("respuesta1")
            respuesta2 = request.form.get("respuesta2")
            respuesta3 = request.form.get("respuesta3")
            respuesta4 = request.form.get("respuesta4")
            tema = request.form.get("tema")
            try:
                if preguntaWeb!="" and respuesta1!="" and respuesta2!="" and respuesta3!="" and respuesta4!="":
                    pregunta.crearPregunta(preguntaWeb,respuesta1,respuesta2,respuesta3,respuesta4,tematica.listarIdTemaTematica(tema))
                    conexion.commit()
                    log.information("El usuario "+usuarioConectado+" ha creado una nueva pregunta.")
                    mensajeControl="Pregunta creada con exito"
                else:
                    error="Los campos no pueden estar vacios"
                    log.error("ERROR: Los campos de las preguntas estan vacios.")
            except:
                error="Error en la creacion de la pregunta"
                log.error("ERROR: No se pudo crear la pregunta.")
    #------------------------------------------------#
            
    return render_template('axon9.html',error=error,mensajeControl=mensajeControl,arrayTemas=arrayTemas)
#----------------------------------------------------------------------

#----------------VISOR-DE-GRUPOS----------------------------------------
@app.route('/puntuacionesGrupo',methods=['GET', 'POST'])
def puntuacionesGrupo():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,grupoJugar
    if usuarioConectado=="":
        return redirect("/")
    error=""
    #------------------------------------------------#
    
    try:
        arrayUsuario=[]
        arrayPuntuacion=[]
        nombreGrupo=grupo.listarNombreGrupo(grupoJugar)
        idGrupo=grupoJugar
        
        arrayUsuarioPuntuacion=grupo.listarUsuarioPuntuacionGrupo(idGrupo)
        
        lenghtUsarioGrupoPuntuacion=len(arrayUsuarioPuntuacion)
        
        for x in range(0,lenghtUsarioGrupoPuntuacion):
            arrayUsuario.append(usuario.listarNombre(arrayUsuarioPuntuacion[x][0]))
            arrayPuntuacion.append(arrayUsuarioPuntuacion[x][1])
    except:
        error="No existe el grupo"
        log.error("ERROR: No existe el grupo.")
        
    return render_template('axon10.html',lenghtUsarioGrupoPuntuacion=lenghtUsarioGrupoPuntuacion,nombreGrupo=nombreGrupo,arrayUsuario=arrayUsuario,arrayPuntuacion=arrayPuntuacion)
#----------------------------------------------------------------------

#----------------ADMISTRACION-DE-GRUPOS--------------------------------
@app.route('/grupoAdmin',methods=['GET', 'POST'])
def grupoAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,grupoJugar,error
    if usuarioConectado!="admin":
        return redirect("/")
    error=""
    #------------------------------------------------#
    
    #-- lista todos los grupos de la base de datos --#
    listadoGrupos=grupo.listarGrupos()
    lenghtListadoGrupos=len(listadoGrupos)
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #--   crear una pregunta con sus respuestas    --#
    data = request.form
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        for x in range(0,lenghtListadoGrupos):
            if "Borrar Grupo" == request.form.get(str(x)):
                grupoBorrar=listadoGrupos[x][0]
                idGrupoBorrar=grupo.listarIdGrupoNombre(grupoBorrar)
                
                arrayUsuariosGrupo=grupo.listarUsuarioGrupos(idGrupoBorrar)
                try:
                    for x in arrayUsuariosGrupo:
                        grupo.borrarUsuarioGrupo(idGrupoBorrar,x[0])
                    grupo.borrarGrupo(idGrupoBorrar)
                    conexion.commit()
                    return redirect("/grupoAdmin")
                except:
                    error="Error en el borrado del grupo"
                    log.error("ERROR: No se pudo crear la pregunta.")
        
        for x in range(0,lenghtListadoGrupos):
            if "Ver Grupo" == request.form.get(str(x)):
                grupoJugar=listadoGrupos[x][0]
                return redirect("/puntuacionesGrupoAdmin")
    #------------------------------------------------#
    
    return render_template('axon11.html',lenghtListadoGrupos=lenghtListadoGrupos,listadoGrupos=listadoGrupos)
#----------------------------------------------------------------------

#----------------ADMISTRACION-DE-USUARIOS------------------------------
@app.route('/usuarioAdmin',methods=['GET', 'POST'])
def usuarioAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,usuarioPerfil
    if usuarioConectado!="admin":
        return redirect("/")
    error=""
    #------------------------------------------------#
    
    #--lista todos los usuarios de la base de datos--#
    listaUsuarios=usuario.listarUsuario()
    lenghtListadoUsuarios=len(listaUsuarios)
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #--   crear una pregunta con sus respuestas    --#
    data = request.form
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        for x in range(0,lenghtListadoUsuarios):
            if "Ver Perfil" == request.form.get(str(x)):
                usuarioPerfil=listaUsuarios[x][0]
                return redirect("/perfilAdmin")
            
#         error="Error en la creacion de la pregunta"
#         log.error("ERROR: No se pudo crear la pregunta.")
    #------------------------------------------------#
            
    return render_template('axon12.html',error=error,lenghtListadoUsuarios=lenghtListadoUsuarios,listaUsuarios=listaUsuarios)
#----------------------------------------------------------------------

#----------------ADMISTRACION-DE-PREGUNTAS-----------------------------
@app.route('/preguntasAdmin',methods=['GET', 'POST'])
def preguntasAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,mensajeControl,idPreguntaConsulta,controlFiltroTema,arrayIdPregunta,arrayPregunta,temaFiltro,controlModificacionPregunta
    if usuarioConectado!="admin":
        return redirect("/")
    error=""
    mensajeControl=""
    idPreguntaConsulta=0
    #------------------------------------------------#
    
    #--Carga los temas a la web y las preguntas sin--#
    #--                   filtro                   --#
    arrayTemas=tematica.listarTematicas()
    
    arrayPreguntas=pregunta.listarIdPreguntaTema()
    lenghtPreguntas=len(arrayPreguntas)
    
    
    if controlModificacionPregunta:
        if len(arrayPregunta)==0:
            for x in range(0,lenghtPreguntas):
                arrayIdPregunta.append(arrayPreguntas[x][0])
                arrayPregunta.append(arrayPreguntas[x][1])
        lenghtPregunta=len(arrayPregunta)
    else:
        arrayPregunta.clear()
        arrayIdPregunta.clear()
        for x in range(0,lenghtPreguntas):
            arrayIdPregunta.append(arrayPreguntas[x][0])
            arrayPregunta.append(arrayPreguntas[x][1])
        lenghtPregunta=len(arrayPregunta)
    #------------------------------------------------#

    #--  Carga la lista de temas de las preguntas  --#
    arrayTema=[]
    for x in range(0,lenghtPreguntas):
        arrayTema.append(arrayPreguntas[x][2])
    #------------------------------------------------#

    #--   Recoge la informacion de la web para     --#
    #--      crear una consultar la pregunta       --#
    data = request.form
    if(len(data)!=0):
        
        if request.form.get("noFiltrar") == "No Filtrar":
            controlModificacionPregunta=True
            controlFiltroTema=0
            arrayPregunta.clear()
            arrayIdPregunta.clear()
            return redirect("/preguntasAdmin")
            
        if request.form.get("filtrar") == "Filtrar":
            controlModificacionPregunta=True
            temaFiltro = request.form.get("tema")
            if temaFiltro!="":
                arrayPregunta.clear()
                arrayIdPregunta.clear()
                for x in range(0,lenghtPreguntas):
                    if tematica.listarIdTemaTematica(temaFiltro)==arrayTema[x]:
                        controlFiltroTema=tematica.listarIdTemaTematica(temaFiltro)
                        arrayIdPregunta.append(arrayPreguntas[x][0])
                        arrayPregunta.append(arrayPreguntas[x][1])
                lenghtPregunta=len(arrayPregunta)
        
        
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        for x in range(0,lenghtPreguntas):
            if request.form.get(str(x)) == "Modificar Pregunta":
                temaFiltro = request.form.get("tema")
                idPreguntaConsulta=arrayIdPregunta[x]
                return redirect("/preguntaConsultaAdmin")
    #------------------------------------------------#
            
    return render_template('axon13.html',error=error,mensajeControl=mensajeControl,arrayPregunta=arrayPregunta,
                           lenghtPregunta=lenghtPregunta,arrayTemas=arrayTemas,temaFiltro=temaFiltro)
#----------------------------------------------------------------------

#----------------VISOR-DE-GRUPOS-ADMIN----------------------------------
@app.route('/puntuacionesGrupoAdmin',methods=['GET', 'POST'])
def puntuacionesGrupoAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,grupoJugar,mensajeControl
    if usuarioConectado!="admin":
        return redirect("/")
    mensajeControl=""
    error=""
    #------------------------------------------------#
    
    try:
        arrayUsuario=[]
        arrayPuntuacion=[]
        nombreGrupo=grupoJugar
        idGrupo=grupo.listarIdGrupoNombre(grupoJugar)
        arrayUsuarioPuntuacion=grupo.listarUsuarioPuntuacionGrupo(idGrupo)
        
        
        lenghtUsarioGrupoPuntuacion=len(arrayUsuarioPuntuacion)
        for x in range(0,lenghtUsarioGrupoPuntuacion):
            arrayUsuario.append(usuario.listarNombre(arrayUsuarioPuntuacion[x][0]))
            arrayPuntuacion.append(arrayUsuarioPuntuacion[x][1])
    except:
        error="No existe el grupo"
        log.error("ERROR: No existe el grupo.")
    data = request.form
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        if request.form.get("cambiarNombre") == "Cambiar Nombre":
            nombreGrupoNuevo = request.form.get("nombreGrupoNuevo")
            try:
                if nombreGrupoNuevo!="":
                    if nombreGrupoNuevo!=nombreGrupo:
                        controlGrupoExiste=False
        
                        for x in range(0,len(grupo.listarGrupos())):
                                        if grupo.listarGrupos()[x][0]==nombreGrupoNuevo:
                                            controlGrupoExiste=True
                                            break
                        if controlGrupoExiste==False:
                            grupo.cambiarNombreGrupo(nombreGrupo,nombreGrupoNuevo)
                            conexion.commit()
                            log.information("Se ha cambiado el nombre del grupo con exito.")
                            mensajeControl="Has cambiado el nombre del grupo con exito"
                            grupoJugar=nombreGrupoNuevo
                            return redirect("/puntuacionesGrupoAdmin")
                        else:
                            error="Ya existe un grupo con ese nombre"
                            log.error("ERROR: Ya existe un grupo con ese nombre.")
                else:
                    error="No se puede cambiar el nombre con un valor vacio"
                    log.error("ERROR: No se puede cambiar el nombre con un valor vacio.")
            except:
                error="No se pudo cambiar el nombre del grupo"
                log.error("ERROR: No se pudo cambiar el nombre del grupo.")
        
        
    return render_template('axon14.html',lenghtUsarioGrupoPuntuacion=lenghtUsarioGrupoPuntuacion,nombreGrupo=nombreGrupo,
                           arrayUsuario=arrayUsuario,arrayPuntuacion=arrayPuntuacion,error=error,mensajeControl=mensajeControl)
#----------------------------------------------------------------------

#----------------PERFIL-PERSONAL-ADMIN---------------------------------
@app.route('/perfilAdmin',methods=['GET', 'POST'])
def perfilAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,usuarioPerfil
    if usuarioConectado!="admin":
        return redirect("/")
    log.information("El admin esta consutando el perfil de " + usuarioPerfil + ".")
    #------------------------------------------------#
    
    data = request.form
    media="Dia"
    
    #--Consulta el id del usuario con el nombre del--#
    #--                   usuario                  --#
    idUsuario=usuario.listarIdUsuarioNombre(usuarioPerfil)
    #------------------------------------------------#
    
    #--   Consulta las medias del usuario actual   --#
    mediaUsuarioGeneral=mediaGeneral(usuario,idUsuario)
    
    arrayTemas=tematica.listarTematicas()
    lenghtArrayTemas=len(arrayTemas)
    
    arrayMediaDia=mediaDiaTemas(usuario,idUsuario,tematica)
    
    arrayMediaMes=mediaMesTemas(usuario,idUsuario,tematica)
    
    arrayMediaAnyo=mediaAnyoTemas(usuario,idUsuario,tematica)
    
    arrayMediaGeneral=mediaGeneralTemas(usuario,idUsuario,tematica)
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #-- redirigirte a otra pagina o consultar una  --#
    #--                   media                    --#
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        media=request.form.get("media")
    #------------------------------------------------#
        
    return render_template('axon15.html',usuarioPerfil=usuarioPerfil,media=media,arrayTemas=arrayTemas,lenghtArrayTemas=lenghtArrayTemas,
                           mediaUsuarioGeneral=mediaUsuarioGeneral,arrayMediaDia=arrayMediaDia,arrayMediaMes=arrayMediaMes,
                           arrayMediaAnyo=arrayMediaAnyo,arrayMediaGeneral=arrayMediaGeneral)
#----------------------------------------------------------------------

#----------------CAMBIAR-CLAVE-----------------------------------------
@app.route('/cambiarClave',methods=['GET', 'POST'])
def cambiarClave():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,usuarioPerfil,error
    if usuarioConectado=="":
        return redirect("/")
    #------------------------------------------------#
    
    mensajeControl=""
    error=""
    data = request.form
        
    #--   Recoge la informacion de la web para     --#
    #--            cambiar la clave                --#
    if(len(data)!=0):
        if request.form.get("cambiarClave")=="Cambiar Clave":
            claveAnterior = request.form.get("textoClaveActual")
            claveNueva = request.form.get("textoClaveNueva")
            try:
                claveActualComprobar=usuario.listarClave(usuarioConectado)
                
                if claveActualComprobar==claveAnterior:
                    if claveNueva!="":
                        usuario.cambiarClaveUsuario(usuarioConectado,claveNueva)
                        conexion.commit()
                        mensajeControl="Ha cambiado su clave con exito"
                        log.information("El usuario "+usuarioConectado+" ha cambiado su clave.")
                    else:
                        error="La contraseña no puede estar vacia"
                    log.error("ERROR: La contraseña introducida por " + usuarioConectado + " esta vacia.")
                else:
                    error="La contraseña actual es erronea"
                    log.error("ERROR: La contraseña introducida por " + usuarioConectado + " actual es erronea.")

            except:
                error="No se encontro pudo cambiar la clave"
                log.error("ERROR: No se encontro pudo cambiar la clave")
    #------------------------------------------------#
    
    return render_template('axon16.html',error=error,mensajeControl=mensajeControl)
#----------------------------------------------------------------------

#----------------AGREGAR-TEMATICA--------------------------------------
@app.route('/tematicaAdmin',methods=['GET', 'POST'])
def tematicaAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,mensajeControl
    if usuarioConectado!="admin":
        return redirect("/")
    log.information("El administrador esta agregando tematicas.")
    #------------------------------------------------#
    
    mensajeControl=""
    error=""
    controlTematicaExiste=False
    controlTematicaVacia=False
    data = request.form
        
    #--   Recoge la informacion de la web para     --#
    #--            agragar un tema                 --#
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        if request.form.get("agregarTematica")=="Agregar Tematica":
            try:
                nuevaTematica = request.form.get("textoNuevaTematica")
                if nuevaTematica=="":
                    controlTematicaVacia=True
                    error="La tematica no puede estar vacia"
                    log.error("ERROR: La tematica no puede estar vacia.")
                arrayTemas=tematica.listarTematicas()
                for x in arrayTemas:
                    if nuevaTematica==x[0]:
                        controlTematicaExiste=True
                        
                if controlTematicaExiste:
                    error="La tematica ya existe"
                    log.error("ERROR: La tematica ya existe.")
                else:
                    if controlTematicaVacia==False:
                        tematica.agregarTematica(nuevaTematica)
                        conexion.commit()
                        mensajeControl="Ha agregado una nueva tematica con exito"
                        log.information("El administrador ha agregado una nueva tematica con exito.")

            except:
                error="No se encontro pudo cambiar la clave"
                log.error("ERROR: No se encontro pudo cambiar la clave")
    #------------------------------------------------#
    
    return render_template('axon17.html',error=error,mensajeControl=mensajeControl)
#----------------------------------------------------------------------

#----------------MODIFICAR-PREGUNTAS------------------------------------
@app.route('/preguntaConsultaAdmin',methods=['GET', 'POST'])
def preguntaConsultaAdmin():
    
    #--Si no tienes una sesion iniciada te redirige--#
    #--      a la pagina de inicio de sesion       --#
    global usuarioConectado,error,mensajeControl,idPreguntaConsulta,controlFiltroTema,controlModificacionPregunta
    if usuarioConectado!="admin":
        return redirect("/")
    error=""
    mensajeControl=""
    controlFiltroTema=0
    #------------------------------------------------#
    
    #--   Recoge la informacion de la web para     --#
    #--   crear una pregunta con sus respuestas    --#
    
    preguntaWeb,respuesta1,respuesta2,respuesta3,respuesta4,correcta,tema=pregunta.listarPreguntaTemaId(idPreguntaConsulta)
    
    nombreTema=tematica.listarTematicaIdTema(tema)
    
    arrayTemas=tematica.listarTematicas()
    
    data = request.form
    if(len(data)!=0):
        if request.form.get("cerrarSesion") == "Cerrar Sesion":
            log.information("El administrador ha cerrado sesion.")
            return redirect("/")
        
        if request.form.get("modificarPregunta")=="Modificar Pregunta":
            preguntaWebNueva = request.form.get("pregunta")
            respuesta1Nueva = request.form.get("respuesta1")
            respuesta2Nueva = request.form.get("respuesta2")
            respuesta3Nueva = request.form.get("respuesta3")
            respuesta4Nueva = request.form.get("respuesta4")
            correctaNueva = request.form.get("correcta")
            temaNueva = request.form.get("tema")
            
            if preguntaWebNueva=="":
                preguntaWebNueva=preguntaWeb
            if respuesta1Nueva=="":
                respuesta1Nueva=respuesta1
            if respuesta2Nueva=="":
                respuesta2Nueva=respuesta2
            if respuesta3Nueva=="":
                respuesta3Nueva=respuesta3
            if respuesta4Nueva=="":
                respuesta4Nueva=respuesta4
            if correctaNueva=="":
                correctaNueva=correcta
            
            print(preguntaWebNueva,respuesta1Nueva,respuesta2Nueva,respuesta3Nueva,respuesta4Nueva,correctaNueva,tematica.listarIdTemaTematica(temaNueva),idPreguntaConsulta)
            
            try:
                pregunta.modificarPregunta(preguntaWebNueva,respuesta1Nueva,respuesta2Nueva,respuesta3Nueva,respuesta4Nueva,correctaNueva,tematica.listarIdTemaTematica(temaNueva),idPreguntaConsulta)
                conexion.commit()
                log.information("El administrador ha modificado una pregunta.")
                mensajeControl="Pregunta modificada con exito"
                controlModificacionPregunta=False
#                 return redirect("/preguntaConsultaAdmin")

            except:
                error="Error en la modificacion de la pregunta"
                log.error("ERROR: No se pudo modificar la pregunta.")
    #------------------------------------------------#
            
    return render_template('axon18.html',error=error,mensajeControl=mensajeControl,arrayTemas=arrayTemas,
                           preguntaWeb=preguntaWeb,respuesta1=respuesta1,respuesta2=respuesta2,respuesta3=respuesta3,
                           respuesta4=respuesta4,correcta=correcta,nombreTema=nombreTema)
#----------------------------------------------------------------------