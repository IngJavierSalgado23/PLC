
__authors__ = 'SMiiCK & Salgado.INC & Parra & Paco'

#Falta borrar subescalon
#La lista simplemente enlazada de raul no sirve, en realidad no es una lista
#Importante Estoy usando Process por lo cual no comparten memoria
#Falta agregar latch,unlatch,contadores y temporizadores
from Tkinter import *
from componente import *
from Node import Node, Lista
import pickle
import cPickle
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from threading import Thread
from multiprocessing import Queue
from multiprocessing import Process
import os
import signal
import time
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8,GPIO.IN)
# GPIO.setup(10,GPIO.IN)
# GPIO.setup(12,GPIO.IN)
# GPIO.setup(40, GPIO.OUT)
# GPIO.output(40, GPIO.LOW)
# GPIO.setup(38, GPIO.OUT)
# GPIO.output(38, GPIO.LOW)
# GPIO.setup(36, GPIO.OUT)
# GPIO.output(36, GPIO.LOW)
def acvtivateSteps():
    global steps, Rung
    cont = Rung
    for i in range (0,cont+1):
        steps[i] = True
    return
def count_steps():
    global steps
    count = 1
    for step in steps:
        if(steps[step] == True):
            count +=1
    return count
def inicia_thread_run():
    global listaFiguras
    global steps
    comenzar = True
    for figura in listaFiguras:
        if(figura.getId()== '-1'):
            print(figura.getFigura())
            print("No se han inicializado todas las entradas")
            comenzar = False
            break
    if (steps[1] == False):
        comenzar = False
        print("No esta inicializado los escalones")
    if(comenzar == True):
        botonRun.pack_forget()
        botonStop.pack(side=RIGHT)
        print("Comenzando Thread")
        run_Thread = Process(target=run, args=(queue_run,))
        run_Thread.daemon = True
        run_Thread.start()
def stop_thread():
    global queue_run
    print('pid programa', os.getpid())
    if(queue_run.empty()==False):
        pid = queue_run.get()
        try:
            os.kill(pid, signal.SIGKILL)
            matar_proceso = ("Se elimino exitosamente el proceso {0}").format(pid)
            print(matar_proceso)
            botonStop.pack_forget()
            botonRun.pack(side=RIGHT)
            
        except:
            print("Error. No se pudo matar el proceso")
def set_up():
    global dir_salidas
    global dir_entradas
    for salida in dir_salidas:
        dir_salidas[salida] = 0
    for entrada in dir_entradas:
        dir_entradas[entrada] = 0
    for latch in dir_latchs:
        dir_latchs[latch] = 0
    for counter in dir_counters:
        dir_counters[counter] = 0
        dir_counters_estados[counter] = 0
    makeNodos()

def help():
    top = Toplevel()
    top.title('Help?')
    top.geometry('400x200')
    label = Label(top, text='Help will come to those who ask', font=2, height=50, width=50)
    label.pack(side=TOP)

def newRung():
    global Rung
    global listaFiguras
    global listaRepetidos
    idBasura = -2
    if (Rung < max_Steps) :
        acvtivateSteps()
        rung = Rung
        idOrg = rung + 30000000
        tempoComponente = componente(idBasura, 0, -1, 0,rung,Rung * y_space,windowWidth,Rung * y_space, -3,-3,"Escalon", 'red',False,idOrg)
        if (checarRepetido(idOrg) == False):
            listaRepetidos.append(idOrg)
            listaFiguras.append(tempoComponente)
            repaint()
            Rung += 1

def newBranch():
    global Rung
    rung = radx.get()
    n1=spinA.get()
    n2=spinB.get()
    if(n1>=max_components-2 or n2>=max_components-1):
        print('opcion invalida')
        return
    n1 = cords[n1]
    n2 = cords[n2]
    if(rung!=0 and steps[rung]):
        tempo_X1 = n1-10
        tempo_X2 = n2+10
        dist_X = (tempo_X2-tempo_X1)
        tempo_x_space = (dist_X/max_Subcomponents)/(spinB.get()-spinA.get())
        tempo_Y1 = (rung*y_space)
        tempo_Y2 = (rung*y_space)+y_space/2
        dist_Y = tempo_Y2-tempo_Y1
        initial_xpad = 5
        idOrgN1 = (rung *1000000)+ spinA.get()
        idOrgN2 = (rung*1000000)+spinB.get()
        if(checarRepetido(idOrgN1) == False and checarRepetido(idOrgN2) == False):
            xline = componente(-2,-1,-1,rung,tempo_X1,(rung*y_space)+y_space/2,tempo_X2,(rung*y_space)+y_space/2,-2,-2,"SubEscalon", 'green',False,idOrgN1 )
            yNode1 = componente(-2,-1,-1,rung,n1-10,(rung*y_space),n1-10, (rung*y_space)+y_space/2,-2,-2,"Nodo",'green',False,idOrgN1)
            yNode2 = componente(-2,-1,-1,rung,n2+10,(rung*y_space),n2+10, (rung*y_space)+y_space/2,-2,-2,"Nodo",'green',False,idOrgN1)
            listaRepetidos.append(idOrgN1)
            listaRepetidos.append(idOrgN2)
            listaFiguras.append(xline)
            listaFiguras.append(yNode1)
            listaFiguras.append(yNode2)
            x1 = (tempo_X1)+ initial_xpad
            y1 = ((rung * y_space) + y_space / 4)+5
            x2 = (tempo_x_space+tempo_X1)- initial_xpad
            y2 = (rung * y_space) + y_space/2 + dist_Y/4
            tam = (max_Subcomponents*(spinB.get()-spinA.get()))
            for i in range (0,tam):
                t_componente = componente(-2,-1,-1,rung,x1,y1,x2,y2,spinA.get(),spinB.get(),"SubComponente",'white',False,idOrgN1)
                listaFiguras.append(t_componente)
                x1 += tempo_x_space
                x2 += tempo_x_space
            repaint()

def newIfClosed():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    col = spinx.get()
    if(col>=9 or col <0):
        print("Opcion Invalida")
        return
    n1 = cords[col]
    n2 = cords[col+1]
    rung = radx.get()
    if rung == 0:
        pass
    else:
        if steps[rung] and col < max_entradas+1:
            idOrg = (rung*100)+col
            tempoComponente = componente(idBasura,0,col,rung,n1+(x_space/4),(rung*y_space)+y_space/4,n2-(x_space/4),(rung*y_space)-y_space/4,
                                         col,col+1,"Abierto",'red',False,idOrg)
            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()

def newIfOpen():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    col = spinx.get()
    if(col>=9 or col <0):
        print("Opcion invalida")
        return
    n1 = cords[col]
    n2 = cords[col+1]
    rung = radx.get()
    if rung == 0:
        pass
    else:
        if steps[rung] and col < max_entradas+1:
            idOrg = (rung*100)+col
            tempoComponente = componente(idBasura,0,col,rung,n1 + (x_space / 4),rung * y_space- y_space / 4, n2 - (x_space / 4),(rung * y_space) + y_space / 4,
                                         col,col+1,"Cerrado",'red',False,idOrg)
            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()

def newOutput():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    rung = radx.get()
    y_padding = 25
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+10000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,x_space*(max_components-2)+y_padding,(rung*y_space)+y_space/3,x_space*(max_components-1)+y_padding,
                                         rung * y_space - y_space / 3,-1,-1,"Salida",'royalblue',False,idOrg)

            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()
def newLatch():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    rung = radx.get()
    y_padding = 25
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+10000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,x_space*(max_components-2)+y_padding,(rung*y_space)+y_space/3,x_space*(max_components-1)+y_padding,
                                         rung * y_space - y_space / 3,-1,-1,"Latch",'royalblue',False,idOrg)
            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()
def newUnlatch():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    rung = radx.get()
    y_padding = 25
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+10000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,x_space*(max_components-2)+y_padding,(rung*y_space)+y_space/3,x_space*(max_components-1)+y_padding,
                                         rung * y_space - y_space / 3,-1,-1,"Unlatch",'royalblue',False,idOrg)

            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()
def newTimer():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    rung = radx.get()
    col = max_components-2
    n1 = cords[col]
    n2 = cords[col+1]
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+100000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,n1 + (x_space / 4),(rung*y_space)+y_space/4,n2 - (x_space / 4),
                                         rung * y_space - y_space /4,-1,-1,"Temporizador",'red',False,idOrg)

            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()
def newCounter():
    global listaFiguras
    global listaRepetidos
    idBasura = 0
    rung = radx.get()
    y_padding = 25
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+10000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,x_space*(max_components-2)+y_padding,(rung*y_space)+y_space/3,x_space*(max_components-1)+y_padding,
                                         rung * y_space - y_space / 3,-1,-1,"Counter",'royalblue',False,idOrg)

            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()
def newReset():
    global listaFiguras
    global listaRepetidos
    idBasura = -1
    rung = radx.get()
    y_padding = 25
    if rung == 0:
        pass
    else:
        if steps[rung]:
            idOrg = (rung+10000)
            tempoComponente = componente(idBasura,0,spinx.get(),rung,x_space*(max_components-2)+y_padding,(rung*y_space)+y_space/3,x_space*(max_components-1)+y_padding,
                                         rung * y_space - y_space / 3,-1,-1,"Reset",'royalblue',False,idOrg)

            if(checarRepetido(idOrg) == False):
                listaRepetidos.append(idOrg)
                listaFiguras.append(tempoComponente)
                repaint()

def checarRepetido(idOrg):
    global listaRepetidos
    for num in listaRepetidos:
        if (num == idOrg):
            print("Repetido")
            return True
            break
    return False

def imprime():
    global listaRepetidos
    print('imprimiendo')
    for id in listaRepetidos:
        print(id)

def repaint():
    #imprime()
    canvas.delete("all")
    #print("El tamano de la lista Oficial" , len(listaFiguras))
    if(len(listaFiguras)>0):
        for figura in listaFiguras:
            if(figura.getFigura() == "Abierto"):
                fig = canvas.create_rectangle(figura.getx1(), figura.gety1(),figura.getx2(),figura.gety2(),fill='white', outline=figura.getColor())
                if('l' in figura.getId()):
                    id = figura.getId()
                    id = id[1:]
                    canvas.create_text((figura.getx1() + figura.getx2()) / 2, (figura.gety1() + figura.gety2()) / 2,
                                       text=('{0} L').format(id))
                elif('c' in figura.getId()):
                    id = figura.getId()
                    id = id[1:]
                    canvas.create_text((figura.getx1() + figura.getx2()) / 2, (figura.gety1() + figura.gety2()) / 2,
                                       text=('{0} C').format(id))
                else:
                    canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = figura.getId())
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura() == "Cerrado"):
                fig = canvas.create_rectangle(figura.getx1(), figura.gety1(), figura.getx2(), figura.gety2(), fill = 'white',outline=figura.getColor())
                canvas.create_line(figura.getx1(),figura.gety2(),figura.getx2(),figura.gety1(),fill=figura.getColor())
                if('l' in figura.getId()):
                    id = figura.getId()
                    id = id[1:]
                    canvas.create_text((figura.getx1() + figura.getx2()) / 2, (figura.gety1() + figura.gety2()) / 2,
                                       text=('{0} L').format(id))
                elif('c' in figura.getId()):
                    id = figura.getId()
                    id = id[1:]
                    canvas.create_text((figura.getx1() + figura.getx2()) / 2, (figura.gety1() + figura.gety2()) / 2,
                                       text=('{0} C').format(id))
                else:
                    canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = figura.getId())
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura()=="Salida"):
                fig = canvas.create_oval(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = figura.getId())
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura()=="Escalon" or figura.getFigura()=="SubEscalon"):
                canvas.create_line(figura.getx2(), figura.gety1(), figura.getx1(), figura.gety2(), fill=figura.getColor())
            elif(figura.getFigura()=="Nodo"):
                fig = canvas.create_line(figura.getx2(), figura.gety1(), figura.getx1(), figura.gety2(), fill=figura.getColor())
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura() == "SubComponente"):
                fig = canvas.create_rectangle(figura.getx1(), figura.gety1(), figura.getx2(), figura.gety2(),
                                        outline=figura.getColor(),tags= "fig")
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: seleccion(event, arg))
            elif(figura.getFigura()=="Temporizador"):
                fig = canvas.create_rectangle(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,figura.gety2()-y_space/4,text = figura.getId())
                canvas.create_image((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,image= imagen_temporizador)
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: poner_timer(event, arg))
            elif(figura.getFigura()=="Latch"):
                id = figura.getId()
                fig = canvas.create_oval(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = ('{0} L').format(id))
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura()=="Unlatch"):
                id = figura.getId()
                fig = canvas.create_oval(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = ('{0} U').format(id))
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))
            elif(figura.getFigura()=="Counter"):
                id = figura.getId()
                fig = canvas.create_oval(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = ('{0} C').format(id))
                canvas.create_text((figura.getx1()+figura.getx2())/2,figura.gety2()-y_space/4,text = figura.getLimit())
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: poner_counter(event, arg))
            elif(figura.getFigura()=="Reset"):
                id = figura.getId()
                fig = canvas.create_oval(figura.getx2(),figura.gety1(),figura.getx1(),figura.gety2(),fill='white',outline=figura.getColor())
                canvas.create_text((figura.getx1()+figura.getx2())/2,(figura.gety1() + figura.gety2())/2,text = ('{0} R').format(id))
                canvas.tag_bind(fig, '<ButtonPress-3>', lambda event, arg=figura: ponerID(event, arg))

def seleccion(event,fig):
    global listaFiguras
    global listaSeleccion
    if(rady.get()==1and len(listaSeleccion)<1):
        fig.setSeleccion(True)
        fig.setColor("yellow")
        print(fig.getInicio(),fig.getFinal(),fig.getFigura())
        for figura in listaFiguras:
            if(figura.getx1()==fig.getx1()):
                label_Componente.pack()
                opcion_texto.pack()
                boton_get.pack()
                listaSeleccion.append(fig)
                break
        repaint()

def ponerID(event,fig):
    global listaSeleccion
    if(rad_opcion.get()==2 ):
        #listaSeleccion.append(fig)
        borrar(fig)
    elif(rad_opcion.get()== 3):
        borrar_subescalon(fig)
    elif(rad_opcion.get()==1 and len(listaSeleccion)<1 and fig.getFigura()!="Nodo" and rad_opcion.get()!=2):
        fig.setSeleccion(True)
        fig.setColor("black")
        listaSeleccion.append(fig)
        repaint()
        label_Id.pack()
        opcion_texto.pack()
        boton_getID.pack()
def poner_timer(event,fig):
    global listaSeleccion
    if (rad_opcion.get() == 2):
        borrar(fig)
    elif (rad_opcion.get() == 1 and len(listaSeleccion) < 1 and fig.getFigura() != "Nodo" and rad_opcion.get() != 2):
        fig.setSeleccion(True)
        fig.setColor("black")
        listaSeleccion.append(fig)
        repaint()
        label_set_timer.pack()
        opcion_texto.pack()
        boton_set_timer.pack()

def set_timer():
    global listaSeleccion
    id = opcion_texto.get().lower()
    fig = listaSeleccion[0]
    if(id.isdigit()):
        del listaSeleccion[:]
        fig.setID(id)
        fig.setColor('red')
        boton_set_timer.pack_forget()
        opcion_texto.pack_forget()
        opcion_texto.delete(0, 'end')
        label_set_timer.pack_forget()
        label_error.pack_forget()
        repaint()
    else:
        label_error.pack()
        opcion_texto.delete(0, 'end')
def poner_counter(event,fig):
    global listaSeleccion
    if (rad_opcion.get() == 2):
        borrar(fig)
    elif (rad_opcion.get() == 1 and len(listaSeleccion) < 1 and fig.getFigura() != "Nodo" and rad_opcion.get() != 2):
        fig.setSeleccion(True)
        fig.setColor("black")
        listaSeleccion.append(fig)
        repaint()
        label_Id.pack()
        opcion_texto.pack()
        label_set_counter.pack()
        opcion_counter.pack()
        boton_set_counter.pack()
def set_Counter():
    global listaSeleccion
    id = opcion_texto.get().lower()
    limite = opcion_counter.get()
    error = False
    id_valido = False
    if(is_number(limite)== False):
        error = True
    fig = listaSeleccion[0]
    if(fig.getFigura()=='Counter'):
        id_tempo = id[:1]
        id_number = id[1:]
        if(is_number(id_number) == True and id_tempo == 'c'):
            if(int(id_number)>=0 and int(id_number)<=99):
                id_valido = True
    if(id_valido == True and error == False):
        del listaSeleccion[:]
        fig.setID(id)
        fig.setLimit(limite)
        fig.setColor('red')
        boton_set_counter.pack_forget()
        label_set_counter.pack_forget()
        opcion_counter.delete(0,'end')
        opcion_counter.pack_forget()
        opcion_texto.delete(0, 'end')
        opcion_texto.pack_forget()
        label_Id.pack_forget()
        label_error.pack_forget()
        repaint()
    else:
        label_error.pack()
        opcion_texto.delete(0, 'end')

def getID():
    global listaSeleccion
    id = opcion_texto.get().lower()
    id_valido = False
    fig = listaSeleccion[0]
    if((fig.getFigura() == "Abierto" or fig.getFigura() == "Cerrado")):
        for i in range(0, max_entradas_pi):
            if (lista_entradas_pi[i] == id):
                id_valido = True
        if(id_valido == False):
            id_tempo = id[:1]
            id_number = id[1:]
            if (is_number(id_number) == True and id_tempo == 'l'):
                if (int(id_number) >= 0 and int(id_number) <= 999):
                    id_valido = True
        if(id_valido == False):
            id_tempo = id[:1]
            id_number = id[1:]
            if (is_number(id_number) == True and id_tempo == 'z'):
                if (int(id_number) >= 0 and int(id_number) <= 99):
                    id_valido = True
        if(id_valido == False):
            id_tempo = id[:1]
            id_number = id[1:]
            if (is_number(id_number) == True and id_tempo == 'c'):
                if (int(id_number) >= 0 and int(id_number) <= 99):
                    id_valido = True
    elif(fig.getFigura()=='Salida'):
        id_tempo = id[:1]
        id_number = id[1:]
        if(is_number(id_number) == True and id_tempo == 'z'):
            if(int(id_number)>=0 and int(id_number)<=99):
                id_valido = True
    elif(fig.getFigura()=='Reset'):
        id_tempo = id[:1]
        id_number = id[1:]
        if(is_number(id_number) == True and id_tempo == 'c'):
            if(int(id_number)>=0 and int(id_number)<=99):
                id_valido = True
    elif(fig.getFigura()=='Latch' or fig.getFigura()=='Unlatch'):
        id_tempo = id[:1]
        id_number = id[1:]
        if(is_number(id_number) == True and id_tempo == 'l'):
            if(int(id_number)>=0 and int(id_number)<=999):
                id_valido = True
    if(id_valido == True):
        del listaSeleccion[:]
        fig.setID(id)
        fig.setColor('red')
        boton_getID.pack_forget()
        opcion_texto.delete(0, 'end')
        opcion_texto.pack_forget()
        label_Id.pack_forget()
        label_error.pack_forget()
        repaint()
    else:
        label_error.pack()
        opcion_texto.delete(0, 'end')

def getComponente():
    value = (opcion_texto.get())
    print(value,len(listaSeleccion))
    if(str(value).lower() == "abierto" ):
        fig = listaSeleccion[0]
        fig.setFigura("Abierto")
        fig.setColor('red')
        boton_get.pack_forget()
        opcion_texto.pack_forget()
        label_Componente.pack_forget()
        label_error.pack_forget()
        del listaSeleccion[:]
        opcion_texto.delete(0, 'end')
        repaint()
    elif (str(value).lower()== "cerrado"):
        fig = listaSeleccion[0]
        fig.setFigura("Cerrado")
        fig.setColor('red')
        boton_get.pack_forget()
        opcion_texto.pack_forget()
        label_Componente.pack_forget()
        label_error.pack_forget()
        del listaSeleccion[:]
        opcion_texto.delete(0, 'end')
        repaint()
    else:
        opcion_texto.delete(0, 'end')
        label_error.pack()
        print("Opcion invalida")
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def borrar(fig):
    global listaFiguras
    global listaRepetidos
    #print(len(listaFiguras),'Tamano de la lista')
    del listaRepetidos[:]
    for figura in listaFiguras:
        if(figura.getx1()==fig.getx1() and figura.gety1() == fig.gety1()):
            if(figura.getIDorg()>=1000000 and figura.getIDorg()<30000000):
                figura.setFigura("SubComponente")
                figura.setColor('white')
                break
            else:
                for id in listaRepetidos:
                    if (fig.getIDorg() == id):
                        listaRepetidos.remove(id)
                        break
                listaFiguras.remove(figura)
                print("Se removio exitosamente")
                break
    repaint()
def borrar_subescalon(fig):
    global listaFiguras
    global listaRepetidos
    cont = 0
    contb=0
    posi = 0
    if (rad_opcion.get() == 3):
        id = fig.getIDorg()
        id_NodoB = None
        tam = len(listaFiguras)
        while(contb<tam):
            figura = listaFiguras[posi]
            contb+=1
            posi+=1
            if (figura.getIDorg() == id):
                listaFiguras.remove(figura)
                cont += 1
                #contb+=1
                posi-=1
                if (figura.getFigura() != "Nodo" and figura.getFigura() != "SubEscalon"):
                    id_NodoB = figura.getFinal()
        for num in listaRepetidos:
            if (num == id or num == id_NodoB):
                listaRepetidos.remove(num)
    repaint()
def save_file():
    global listaFiguras
    print("Saving file")
    url = str(asksaveasfilename())
    cPickle.dump(listaFiguras, open(("{0}.p").format(url), 'wb'))

def load_file():
    print("loading file")
    global listaFiguras
    global steps
    global Rung
    global listaSeleccion
    del listaSeleccion[:]
    del listaFiguras[:]
    global listaRepetidos
    del listaRepetidos[:]
    cont = 0
    url = askopenfilename()
    listaFiguras = pickle.load(open(str(url),"rb"))
    repaint()
    ##Refresh steps
    for step in steps:
        steps[step] = False
    for figuras in listaFiguras:
		if(figuras.getIDorg()>=30000000):
			cont +=1
    Rung = cont + 1
    acvtivateSteps()
    for figura in listaFiguras:
        listaRepetidos.append(figura.getIDorg())

def makeNodos():
    global listaFiguras
    global lista_de_Nodos
    global max_Steps
    count = 1
    steps_activados = count_steps()
    while count < steps_activados-1:
        new_Nodo = Node(count, None, None)
        for comp in listaFiguras:
            figura = comp.figura
            if comp.escalon == count and (figura == 'Abierto' or figura == 'Cerrado'):
                new_Nodo.listaEntradas.append(comp)
            elif comp.escalon == count and (figura == 'Salida' or figura == 'Latch' or figura == 'Unlatch' or figura == 'Counter' or figura == 'Reset'):
                new_Nodo.salida = comp
            elif comp.escalon == count and (figura == 'Temporizador'):
                new_Nodo.timer = comp
        lista_de_Nodos.agregar(new_Nodo)
        count += 1

def run(queue_run):
    queue_run.put(os.getpid())
    print(os.getpid(), "Mi pid run")
    set_up()
    global lista_de_Nodos
    while (True):
        nodo = lista_de_Nodos.getHead()
        while(nodo != None and nodo.salida !=  None):
            actualizar_estados(nodo)
            print("antes de hacer operacion", dir_latchs['l1'])
            nodo.make_operacion()
            print ("Salida", nodo.salida.getId(), nodo.salida.getEstado())
            if(nodo.timer !=None):
                print('Durmiendo', nodo.timer.getId())
                time.sleep(float(nodo.timer.getId()))
            actualizar_salida(nodo)
            nodo = nodo.get_siguiente()
        time.sleep(0.1)

def actualizar_salida(nodo):
    global dir_salidas
    #print("Soy el nodo", nodo.data,nodo.salida.getEstado(),nodo.salida.getFigura())
    id = nodo.salida.getId()
    if('z' in id):
        for salida in dir_salidas:
            if(salida == nodo.salida.getId()):
                dir_salidas[salida] = nodo.salida.getEstado()
    elif ('l' in id):
        if(nodo.salida.getFigura()=='Latch' and nodo.salida.getEstado()==1):
            for latch in dir_latchs:
                if(latch == nodo.salida.getId()):
                    dir_latchs[latch] = 1
                    break
        else:
            for latch in dir_latchs:
                if(nodo.salida.getEstado()== 0):
                    break
                if(latch == nodo.salida.getId()):
                    dir_latchs[latch] = 0
                    break
    elif ('c' in id):
        if(nodo.salida.getFigura()=='Counter' and nodo.salida.getEstado()==1):
            for counter in dir_counters:
                if(counter == nodo.salida.getId()):
                    dir_counters[counter] = int(dir_counters[counter]) + 1
                    if(dir_counters[counter] == nodo.salida.getLimit()):
                        dir_counters_estados[counter] = 1
                    break
        else:
            for counter in dir_counters:
                if(nodo.salida.getEstado()== 0):
                    break
                if(counter == nodo.salida.getId()):
                    dir_counters_estados[counter] = 0
                    dir_counters[counter] = 0
                    break
    print('salida', 'z0',dir_salidas['z0'],'z1',dir_salidas['z1'],'z2',dir_salidas['z2'])
    print('c1',dir_counters_estados['c1'],dir_counters['c1'], 'c2', dir_counters_estados['c2'],dir_counters['c2'])
    print('l1',dir_latchs['l1'])

    # if (dir_salidas["z0"]==0):
		# GPIO.output(36, GPIO.LOW)
    # elif (dir_salidas["z0"]==1):
	 #    GPIO.output(36, GPIO.HIGH)
    # if (dir_salidas["z1"]==0):
		# GPIO.output(38, GPIO.LOW)
    # elif (dir_salidas["z1"]==1):
	 #    GPIO.output(38, GPIO.HIGH)
    # if (dir_salidas["z2"]==0):
		# GPIO.output(40, GPIO.LOW)
    # elif (dir_salidas["z2"]==1):
	 #   GPIO.output(40, GPIO.HIGH)
def actualizar_estados(nodo):
    #Se supone que aqui los lee de la Pi
    global dir_salidas
    global dir_entradas
    # if ( GPIO.input(8)):
    #   dir_entradas[0]=1
    # else:
		# dir_entradas[0]=0
    # if ( GPIO.input(10)):
    #   dir_entradas[1]=1
    # else:
		# dir_entradas[1]=0
    # if ( GPIO.input(12)):
    #   dir_entradas[2]=1
    # else:
		# dir_entradas[2]=0
    dir_entradas[0] = 1
    dir_entradas[1] = 0
    dir_entradas[2] = 1
    # for figura in nodo.listaEntradas:
    #     if(figura.getId() == '0'):
    #         figura.setEstado(dir_entradas[0])
    #     elif (figura.getId() == '1'):
    #         figura.setEstado(dir_entradas[1])
    #     elif (figura.getId() == '2'):
    #         figura.setEstado(dir_entradas[2])
    #     elif(figura.getId())
    #     if(figura.getFigura() == 'Cerrado'):
    #         estado = figura.getEstado()
    #         if(estado == 0):
    #             figura.setEstado(1)
    #         elif(estado == 1):
    #             figura.setEstado(0)
    #         else:
    #             print("Error entrada no inicializada")

    # print('entradas',dir_entradas)
    for figura in nodo.listaEntradas:
        opcion = str(figura.getId())
        opcion = opcion.lower()
        if('z' in opcion):
            figura.setEstado(dir_salidas[opcion])
            #print(figura.getEstado(), 'Estado', 'Soy salida', figura.getFigura(),figura.getId())
        elif('l' in opcion):
            figura.setEstado(dir_latchs[opcion])
            #print(figura.getEstado(), 'Estado', 'Soy latch', figura.getFigura(), figura.getId())
        elif('c' in opcion):
            figura.setEstado(dir_counters_estados[opcion])
            #print(figura.getEstado(), 'Estado', 'Soy counter', figura.getFigura(), figura.getId())
        else:
            figura.setEstado(dir_entradas[int(opcion)])
            #print(figura.getEstado(), 'Estado', 'Soy Entrada', figura.getFigura())
        if (figura.getFigura() == 'Cerrado'):
            estado = figura.getEstado()
            if(estado == 0):
                    figura.setEstado(1)
            elif(estado == 1):
                    figura.setEstado(0)
            else:
                print("Error entrada no inicializada")




window = Tk()
window.title('Raspberry Pi PLC')
window.attributes('-zoomed', True)
windowWidth = window.winfo_screenwidth()
windowHeight = window.winfo_screenheight()
canvas = Canvas(window, bg='white')

queue_run = Queue()

#Automatizacion
max_components = 11 #Espacio blanco para separar salidas y entradas
max_entradas = 9
max_Steps = 15
max_Subcomponents = 4
max_salidas_pi = 3
max_entradas_pi = 3
x_space = windowWidth/max_components
y_space = windowHeight/(max_Steps+1)
x_Mouse= 0
y_Mouse= 0
Rung = 1
steps={}
dir_entradas = {}
dir_salidas = {}
dir_latchs = {}
dir_counters = {}
dir_counters_estados = {}
listaFiguras = list()
listaRepetidos = list()
listaSeleccion = list()
lista_de_Nodos = Lista()
lista_entradas_pi = list()
lista_salidas_pi = list()
lista_salidas = list()
lista_latch = list()

for i in range (0,max_entradas_pi):
    lista_entradas_pi.append(str(i))
    dir_entradas[i] = 0
for i in range(0,99):
    lista_salidas_pi.append(('z{0}').format(i))
    dir_salidas[('z{0}').format(i)] = 0
for i in range (1,max_Steps):
    steps[i] = False
for i in range (0,999):
    lista_latch.append(('l{0}').format(i))
    dir_latchs[('l{0}').format(i)] = 0
for i in range(0,9):
    dir_counters[('c{0}').format(i)] = 0
    dir_counters_estados[('c{0}').format(i)] = 0

print('Directorios de latches',len(dir_latchs))
initial_xspace = 25;
cords = {0:0,1:initial_xspace}
cords_b = {0:4,1:initial_xspace +4}
line_spacer = x_space / 2

for i in range(2, max_components):
    cords[i] = cords[i - 1] + x_space
    cords_b[i] = cords_b[i - 1] + x_space

#Frames
f1 = Frame(window, bg='royalblue')
f2 = Frame(window, bg='cyan')
f3 = Frame(window, width=25, bg='lightblue')
mbFile = Menubutton(f1, text='File', relief=RAISED, activebackground='lightgray')
options = Menu(mbFile, tearoff=0)
mbFile.config(menu=options)
options.add_command(label='Force Quit',  command=window.quit)
options.add_command(label='Load',  command=load_file)
options.add_command(label='Save', command=save_file)

mbView = Menubutton(f1, text='Views', relief=RAISED, activebackground='lightgray')
mbTools = Menubutton(f1, text='Tools', relief=RAISED, activebackground='lightgray')
mbHelp = Menubutton(f1, text='Help', relief=RAISED, activebackground='lightgray')
optionsHelp = Menu(mbHelp, tearoff=0)
mbHelp.config(menu=optionsHelp)
optionsHelp.add_command(label='Help',  command=help)
label_Componente = Label(window,text= "Introduzca el componente que quiera usar")
label_Id = Label(window,text="Introduzca el numero de entrada o salida del componente")
label_set_timer = Label(window,text="Introduzca el tiempo en segundos para el timer")
label_set_counter = Label(window,text='Introduzca el numero a llegar en el contador')
opcion_counter = Entry(window)
opcion_texto = Entry(window)
label_error = Label(window,text = "Opcion invalida")
#Botones

boton_get= Button(window, text="Enter", command=getComponente)
boton_getID= Button(window, text="Enter", command=getID)
boton_set_timer = Button(window,text="Enter",command = set_timer)
boton_set_counter = Button(window,text='Enter',command = set_Counter)
imagenesURL = {1 : 'Imgs/NewRung.png',2:'Imgs/RungBranch.png',3:'Imgs/IfClosed.png', 4:'Imgs/IfOpen.png',5:'Imgs/Output.png',6:'Imgs/OutputLatch.png',
              7:'Imgs/OutputUnlatch.png',8:'Imgs/CountUp.png',9: 'Imgs/Reset.png', 10:'Imgs/Timer.png'}
images = {}
comandos = {1:newRung, 2:newBranch, 3:newIfClosed, 4:newIfOpen, 5:newOutput,6:newLatch,7:newUnlatch,8:newCounter,9:newReset,10:newTimer}
f1.pack(fill=X, side=TOP)
f2.pack(fill=X, side=TOP)
f3.pack(fill=Y, side=LEFT)
botonRun = Button(f3,text="Run",command = inicia_thread_run)
imagen_temporizador = PhotoImage(file= 'Imgs/Timer.png')
botonStop = Button(f3,text="Stop",command = stop_thread)
print(len(imagenesURL))
for i in range (1,len(imagenesURL)+1): #Agrega los botones con sus imagenes
        images[i] = PhotoImage(file=imagenesURL[i])
        tImagen = images[i]
        tComando = comandos[i]
        tempoButton = Button(f2, image=tImagen, command=tComando)
        tempoButton.pack(side=LEFT)
colLabel = Label(f2, text='Col: ', fg='black')
spinx = IntVar()
col = Spinbox(f2,textvariable=spinx,width=2, wrap=TRUE, from_=1, to_=max_components-3)
nodoLabelA = Label(f2, text='Nodo A: ', fg='black')
spinA = IntVar()
nodo1 = Spinbox(f2,textvariable=spinA,width=2, wrap=TRUE, from_=1, to_=max_entradas-1)
nodoLabelB = Label(f2, text='Nodo B: ', fg='black')
spinB = IntVar()
nodo2 = Spinbox(f2,textvariable=spinB,width=2, wrap=TRUE, from_=2, to_=max_entradas)
radx = IntVar()
rady = IntVar()
rad_opcion = IntVar()
for i in range(1,max_Steps):
    Radiobutton(f3, text=str(i),variable=radx,value=i).pack(anchor=W,side=TOP)
Radiobutton(f2,variable=rady,value=1,text="SubEscalon ON").pack(anchor=W,side=RIGHT)
Radiobutton(f2,variable=rady,value=0,text="SubEscalon OFF").pack(anchor=W,side=RIGHT)
Radiobutton(f2,variable=rad_opcion,value=1,text="Asignar Valor ON").pack(anchor=W,side=RIGHT)
Radiobutton(f2,variable=rad_opcion,value=0,text="Asignar Valor OFF").pack(anchor=W,side=RIGHT)
Radiobutton(f2,variable=rad_opcion,value =2,text="Borrar").pack(anchor=W,side=RIGHT)
Radiobutton(f2,variable=rad_opcion,value =3,text="Borrar SubEscalon").pack(anchor=W,side=RIGHT)
colLabel.pack(side=LEFT)
col.pack(side=LEFT)
nodoLabelA.pack(side=LEFT)
nodo1.pack(side=LEFT)
nodoLabelB.pack(side=LEFT)
nodo2.pack(side=LEFT)
mbFile.pack(side=LEFT)
mbView.pack(side=LEFT)
mbTools.pack(side=LEFT)
mbHelp.pack(side=LEFT)
canvas.pack(side=RIGHT, fill=BOTH, expand=1)
botonRun.pack(side=RIGHT)
window.mainloop()
#GPIO.cleanup()face

