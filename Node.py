
class Node(object):

    def __init__(self, d, n = None, salida = None, timer = None):
        self.data = d
        self.siguiente = n
        self.listaEntradas = list()
        self.salida = salida
        self.listaRepetidos = list()
        self.timer = timer
    def __str__(self):
        return str(self.data)
    def checksub(self):
        count = 0
        for x in self.listaEntradas:
            if x.getIDorg() > 999999:
                #return True
                if len(self.listaRepetidos) == 0:
                    self.listaRepetidos.append(x)
                    count += 1
                else:
                    for compi in self.listaRepetidos:
                        if compi.getIDorg() == x.getIDorg():
                            break
                        else:
                            count += 1
                            self.listaRepetidos.append(x)
        return count
    def setFalse(self):
        for compi in self.listaEntradas:
            compi.setFlag(False)
    def make_operacion(self):
        if(len(self.listaEntradas) == 0 and self.salida == None):
            return
        if(len(self.listaEntradas)== 0 and self.salida!= None):
            self.salida.setEstado(1)
        if(self.salida == None):
            print("No hay salida, no realizo operacion")
            return
        cont_subescalon = self.checksub()
        val_int = list()
        print("Subescalones" , cont_subescalon)
        if cont_subescalon > 0: #Para todos los subescalones
            for rep in self.listaRepetidos: #Tomo la referencia de un componente de un subescalon distinto
                Nodo1Temp = rep.getInicio() #Referencia inicial
                Nodo2Temp = rep.getFinal() #Referencia final
                temporalORabajo = 1 #Lo empiezo en 1 para que no me afecte en las operaciones
                temporalORarriba = 1
                print(Nodo1Temp,Nodo2Temp,'Nodos')
                for x in self.listaEntradas: #Aqui se obiene la respuesta de un subescalon
                    if x.getIDorg() == rep.getIDorg(): #Si encuentra un componente con el mismo id que el que se esta evaluando realiza el AND
                        x.setFlag(True) #Marca que ya se evaluo
                        if x.getEstado() != 1:
                            temporalORabajo = 0  #El AND de todos los subcomponentes si alguno es 0 entonces va a ser 0
                    elif  x.getInicio() >= Nodo1Temp and x.getFinal() <= Nodo2Temp: #Busca que componentes que son parte del escalon realizan operacion con un subescalon
                        x.setFlag(True) #Lo marca como visitado
                        print(x.getId(),x.getIDorg(),x.getInicio(),x.getFinal())
                        if x.getEstado() != 1:
                            temporalORarriba = 0
                print('tempoAbajo', temporalORabajo, 'tempoArriba' , temporalORarriba)
                if(temporalORabajo == 1 or temporalORarriba == 1) :
                    AnsTemp =1
                else:
                    AnsTemp = 0
                val_int.append(AnsTemp)
            del self.listaRepetidos[:]#Borrar la lista de repetidos para poder volver a iterar
            AnsEsc = 1
            for componente in self.listaEntradas:
                print(componente.getFlag())
                if componente.getFlag() != True:  #Busca los componentes que no han sido marcados como evaluados
                    componente.setFlag(True)
                    #print(componente.getEstado(), 'estado')
                    if componente.getEstado() != 1:
                        AnsEsc = 0
                        break
            val_int.append(AnsEsc)
            answer = 1
            #print("val len" , len(val_int))
            for val in val_int: #Un ultimo AND
                print(val)
                if val == 0:
                    answer = 0
                    break
            #print('resul', answer)
            self.salida.setEstado(answer)
        else:
            resultado = 1
            for x in self.listaEntradas:
                if x.idOrg < 10000: #Evalua solo las entradas
                    if x.estado == 0:
                        resultado = 0
                        flag_Entrada0 = True
                        break
            self.salida.setEstado(resultado)
        self.setFalse()
        ##Actualizar directorios Importante!!

    def agrega_entrada(self,componente):
        self.listaEntradas.append(componente)

    def get_siguiente(self):
        return self.siguiente

    def set_next(self, n):
        if self.siguiente == None:
            self.siguiente = n
        else:
            self.siguiente.set_next(n)

    def get_data(self):
        return self.data

    def set_data(self, d):
        self.data = d

    def imprime(self):
        print self.data
        if(self.siguiente != None):
            self.siguiente.imprime()
    def buscar(self, indice):
        if indice == self.data:
            return self
        else:
            self.siguiente.buscar(indice)


class Lista(object):
    def __init__(self):
        self.head = None
        self.size = 0
    def agregar(self, nodo):
        if self.head == None:
            self.head = nodo
            self.size += 1
        else:
            self.head.set_next(nodo)
            self.size += 1
    def imprime(self):
        self.head.imprime()
    def buscar(self, referencia, indice):
        if referencia.data == indice:
            return referencia
        else:
            return self.buscar(referencia.siguiente, indice)
    def getHead(self):
        return self.head
#
# uno = Node(1, None, None)
# dos = Node(2, None, None)
# tres =Node(3, None, None)
#
# lista = Lista()
# global busc
# lista.agregar(uno)
# lista.agregar(dos)
# lista.agregar(tres)
# lista.imprime()
# busc = lista.buscar(lista.head, 3)
# busc.imprime()
#
