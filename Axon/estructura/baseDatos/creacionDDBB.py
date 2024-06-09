import sqlite3
from gestorConexion import *

class creacionDDBB():
#----------------CONSTRUCTOR-------------------------------------------
    def __init__(self,conexion,cursor):
        self.conexion=conexion
        self.cursor=cursor
#----------------------------------------------------------------------

#----------------------------------------------------------------------
#----------------------------------------------------------------------
        self.borrarTema="DROP TABLE IF EXISTS tema;"
        self.crearTema='''
        create table tema(
            id integer,
            tematica varchar(50),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.cargarTema='''
        INSERT INTO tema VALUES (NULL,"Geografia e Historia"),
        (NULL,"Matematicas"),(NULL,"Lengua"),(NULL,"Fisica y Quimica")
        '''


        self.borrarUsuario="DROP TABLE IF EXISTS usuario;"
        self.crearUsuario='''
        create table usuario(
            id integer,
            nombre varchar(30),
            clave varchar(10),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.cargarUsuario='''
        INSERT INTO usuario VALUES(NULL,"Hugo","1234"),(NULL,"Martin","1234"),(NULL,"Paco","1234"),(NULL,"Angel","1234"),(NULL,"Luis","1234")
        '''

        self.borrarRespuesta="DROP TABLE IF EXISTS respuesta;"
        self.crearRespuesta='''
        create table respuesta(
            id integer,
            idUsuario integer,
            fecha date,
            idPregunta integer,
            respuestaCorrecta int,
            FOREIGN KEY (idPregunta) REFERENCES pregunta(id),
            FOREIGN KEY (idUsuario) REFERENCES usuario(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        # self.cargarRespuesta='''
        # INSERT INTO perfil VALUES(NULL,1,"2024-05-20",2,0),(NULL,1,"2024-05-20",2,1)
        # '''



        self.borrarAmigo="DROP TABLE IF EXISTS amigo;"
        self.crearAmigo='''
        create table amigo (
            id integer,
            idUsuario1 integer,
            idUsuario2 integer,
            FOREIGN KEY (idUsuario1) REFERENCES usuario(id),
            FOREIGN KEY (idUsuario2) REFERENCES usuario(id),
            CONSTRAINT fk_usuario_unique UNIQUE (idUsuario1, idUsuario2),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        # self.cargarAmigo='''
        # INSERT INTO amigo VALUES(NULL,1,2),(NULL,1,3),(NULL,1,4),(NULL,1,5)
        # '''


        self.borrarGrupo="DROP TABLE IF EXISTS grupo;"
        self.crearGrupo='''
        create table grupo(
            id integer,
            idTema integer,
            nombre varchar(50),
            FOREIGN KEY (idTema) REFERENCES tema(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        # self.cargarGrupo='''
        # INSERT INTO grupo VALUES(NULL,2,"mate")
        # '''

        self.borrarUsuarioGrupo="DROP TABLE IF EXISTS usuarioGrupo;"
        self.crearUsuarioGrupo='''
        create table usuarioGrupo(
            idGrupo integer,
            idUsuario integer,
            puntuacion integer,
            FOREIGN KEY (idUsuario) REFERENCES usuario(id),
            FOREIGN KEY (idGrupo) REFERENCES grupo(id)
        );
        '''
        # self.cargarUsuarioGrupo='''
        # INSERT INTO usuarioGrupo VALUES(1,1,20)
        # '''

        self.borrarPregunta="DROP TABLE IF EXISTS pregunta;"
        self.crearPregunta='''
        create table pregunta(
            id integer,
            pregunta varchar(50),
            respuesta1 varchar(50),
            respuesta2 varchar(50),
            respuesta3 varchar(50),
            respuesta4 varchar(50),
            correcta varchar(50),
            idTema integer,
            FOREIGN KEY (idTema) REFERENCES tema(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.cargarPregunta='''
        INSERT INTO pregunta VALUES
        (NULL,"¿Cual es la capital de España?","Madrid","Sevilla","Barcelona","Valencia","Madrid",1),
        (NULL,"¿Cual es la capital de Portugal?","Lisboa","Oporto","Aveiro","Lagos","Lisboa",1),
        (NULL,"¿Cual es la capital de Alemania?","Berlin","Hamburgo","Munich","Nuremberg","Berlin",1),
        (NULL,"¿Cual es la capital de Francia?","Paris","Nantes","Normandia","Marsella","Paris",1),
        (NULL,"¿Cual es la capital de Polonia?","Varsovia","Cracovia","Lublin","Breslavia","Varsovia",1),
        (NULL,"¿En que continente se encuentra Chipre?","Europa","Africa","Asia","Norte America","Europa",1),
        (NULL,"¿Cuando descubrio Colon America?","1492","1512","1340","1429","1492",1),
        (NULL,"¿Que pais no pertenecia a los aliados en la segunda guerra mundial?","Italia","Francia","Polonia","Estados Unidos","Italia",1),
        (NULL,"¿Cuánto es 45 dividido entre 9?","4","5","6","7","5",2),
        (NULL,"¿Cuánto es 540 dividido entre 5?","108","120","118","110","108",2),
        (NULL,"¿Cuánto es 286 dividido entre 4?","71.5","70","60","64.5","71.5",2),
        (NULL,"¿Cuánto es 98 dividido entre 3?","32.6","33","31.3","30","32.6",2),
        (NULL,"¿Cuánto es 13 multiplicado por 9?","117","118","115","116","117",2),
        (NULL,"¿Cuanto es 62 multiplicado por 5?","310","312","319","320","310",2),
        (NULL,"¿Cuanto es 55 multiplicado por 22?","1210","1012","1220","1110","1210",2),
        (NULL,"¿Cuanto es 428 mas 265 menos 120?","573","602","523","570","573",2),
        (NULL,"¿Cuanto es 981 mas 258 menos 801?","438","568","439","448","438",2),
        (NULL,"¿Cual es el sujeto de la frase: Estuve en el concierto con Marta?","SO yo","Marta","El","Nosotros","SO yo",3),
        (NULL,"¿Cual es el sujeto de la frase: Mis tios compraron los regalos de la fiesta?","Mis tios","los regalos","yo","SO vosotros","Mis tios",3),
        (NULL,"¿Cual es el sujeto de la frase: No sabemos quien rompio el jarron?","SO nosotros","el jarron","el","SO ellos","SO nosotros",3),
        (NULL,"¿Cual es el sujeto de la frase: El doctor me dijo que hablase con la doctora?","El doctor","la doctora","SO yo","me","El doctor",3),
        (NULL,"¿Que clase es la siguiente palabra: con?","Preposicion","Adjetivo","Determinante","Verbo","Preposicion",3),
        (NULL,"¿Que clase es la siguiente palabra: amarillo?","Adjetivo","Preposicion","Verbo","Nombre","Adjetivo",3),
        (NULL,"¿Que clase es la siguiente palabra: volar?","Verbo","Determinante","Adjetivo","Nombre","Verbo",3),
        (NULL,"¿Que sifnifica la palabra: tension?","Estado de un cuerpo sometido a la acción de fuerzas opuestas que lo atraen","Propiedad que permite retornar a un estado anterior","El calor desprendido de dos objetos que colisionan","La fuerza invisible que ejerce un cuerpo por su masa","Estado de un cuerpo sometido a la acción de fuerzas opuestas que lo atraen",3),
        (NULL,"¿Cual es el elemento numero 45 de la tabla periodica?","Rodio","Azufre","Oro","Hidrogeno","Rodio",4),
        (NULL,"¿Cual es el elemento numero 3 de la tabla periodica?","Litio","Rodio","Sodio","Paladio","Litio",4),
        (NULL,"¿Cual es el elemento numero 23 de la tabla periodica?","Vanadio","Cobre","Litio","Oxigeno","Vanadio",4),
        (NULL,"¿Que numero de la tabla periodica es el Oxigeno?","8","24","16","9","8",4),
        (NULL,"¿Que numero de la tabla periodica es el Hidrogeno?","1","2","12","3","1",4),
        (NULL,"¿Que numero de la tabla periodica es el Oro?","79","46","23","34","79",4),
        (NULL,"¿Que numero de la tabla periodica es el Platino?","78","64","70","80","78",4),
        (NULL,"¿Porque cuando sueltas un yunque y una pluma en la luna caen a la vez?","Porque no hay resistencia del aire","Porque en el espacio los objetos no tienen masa","Porque no hay suficiente distancia para que el yunque caiga antes","En la luna no caen a la vez","Porque no hay resistencia del aire",4)
        '''
#----------------------------------------------------------------------
#----------------------------------------------------------------------


#----------------------------------------------------------------------
#----------------------------------------------------------------------
    def crearDDBB(self):
        self.cursor.execute(self.borrarTema)
        self.cursor.execute(self.crearTema)
        self.cursor.execute(self.borrarUsuario)
        self.cursor.execute(self.crearUsuario)
        self.cursor.execute(self.borrarRespuesta)
        self.cursor.execute(self.crearRespuesta)
        self.cursor.execute(self.borrarAmigo)
        self.cursor.execute(self.crearAmigo)
        self.cursor.execute(self.borrarGrupo)
        self.cursor.execute(self.crearGrupo)
        self.cursor.execute(self.borrarUsuarioGrupo)
        self.cursor.execute(self.crearUsuarioGrupo)
        self.cursor.execute(self.borrarPregunta)
        self.cursor.execute(self.crearPregunta)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
#----------------------------------------------------------------------
    def cargarDDBB(self):
        self.cursor.execute(self.cargarTema)
        self.cursor.execute(self.cargarUsuario)
    #     self.cursor().execute(self.cargarRespuesta)
    #     self.cursor().execute(self.cargarAmigo)
    #     self.cursor().execute(self.cargarGrupo)
    #     self.cursor().execute(self.cargarUsuarioGrupo)
        self.cursor.execute(self.cargarPregunta)
#----------------------------------------------------------------------
#----------------------------------------------------------------------