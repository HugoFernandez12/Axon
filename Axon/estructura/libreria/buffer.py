class buffer:

    def __init__(self,num):
        self.almacen = ""
        self.size=num

#----------------------------------------------------------------------
# Crea una trama en la que el mensaje se rodea de ETX y STX
#----------------------------------------------------------------------
    def crearTrama(self,texto):
        texto=chr(2)+texto+chr(3)
        return texto
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Agrega la trama a el buffer para que lo almacene
#----------------------------------------------------------------------
    def añadirTrama(self,texto):
        if((len(self.almacen)+len(texto))<=self.size):
            self.almacen = self.almacen+texto
        else:
            self.almacen=""
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Extrae la primera trama que haya en el buffer
#----------------------------------------------------------------------
    def extraerTrama(self):
        mensaje=""
        controlTrama=0
        controlBorrado=0
        for x in range(0,len(self.almacen)):
            if(self.almacen[x]==chr(2)):
                controlTrama=x
                for y in range(controlTrama+1,len(self.almacen)):
                    if(self.almacen[y]==chr(2)):
                        controlTrama=y
                    elif(self.almacen[y]==chr(3)):
                        controlBorrado=y
                        for z in range(controlTrama+1,y):
                            mensaje=mensaje+self.almacen[z]
                        break
                break
        if(controlBorrado!=0):
            self.almacen=self.almacen[controlBorrado+1:len(self.almacen)]
        return mensaje

#----------------------------------------------------------------------