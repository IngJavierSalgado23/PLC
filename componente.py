class componente(object):

    def __init__(self,id,estado,columna,escalon,x1,y1,x2,y2,nodo_inicio,nodo_final,figura,color,seleccionado,idOrg):
        self.id = id
        self.columna = columna
        self.estado = estado
        self.escalon = escalon
        self.x1 = x1
        self.y1 =y1
        self.x2 = x2
        self.y2 = y2
        self.figura = figura
        self.color = color
        self.seleccionado = seleccionado
        self.idOrg = idOrg
        self.nodo_inicio = nodo_inicio
        self.nodo_final = nodo_final
        self.resuelto = 1
        self.flag = False
        self.limit = 0
    def getLimit(self):
        return int(self.limit)
    def setLimit(self,num):
        self.limit = num
    def getId(self):
        return str(self.id)

    def getCol(self):
        return int(self.columna)

    def getEscalon(self):
        return float(self.escalon)

    def getEstado(self):
        return int(self.estado)

    def setEstado(self, estado):
        self.estado = estado

    def getx1(self):
        return int(self.x1)

    def gety1(self):
        return int(self.y1)

    def getx2(self):
        return float(self.x2)

    def gety2(self):
        return int(self.y2)

    def getFigura(self):
        return str(self.figura)

    def getColor(self):
        return str(self.color)

    def getSeleccion(self):
        return bool(self.seleccionado)

    def getIDorg(self):
        return int(self.idOrg)
    def setFigura(self,figura):
        self.figura = figura
    def getFlag(self):
        return bool(self.flag)
    def setFlag(self,flag):
        self.flag = flag
    def setSeleccion(self,seleccion):
        self.seleccionado = seleccion
    def setColor(self,color):
        self.color = color
    def getIDorg(self):
        return int(self.idOrg)
    def setID(self,id):
        self.id = id
    def getEscalon(self):
        return int(self.escalon)
    def getInicio(self):
        return int(self.nodo_inicio)
    def setInicio(self,inicio):
        self.nodo_inicio = inicio
    def getFinal(self):
        return int (self.nodo_final)
    def setFinal(self,final):
        self.nodo_final = final

