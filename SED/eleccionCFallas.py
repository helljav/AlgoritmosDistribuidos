# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
import random
from eventEleccionFallas import EventEleccionFallas
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation


class ChangRoberts(Model):
    
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.activo = False
        self.banderaLider = self.id
        self.sinVisitar = self.neighbors[:]
        self.estado = "NOLIDER"
        self.ignoraTiempo = False
        self.ok = []
        self.estadoParo = False
        self.estadoAnterior = False


    def mensajes(self, mensaje,tiempo,destino,origen,eleccion):
        """ Se manda a llamar cada vez que se quiere enviar un mensaje"""
        newMessage = EventEleccionFallas(mensaje, tiempo, destino, origen,eleccion)
        #print ("Soy el nodo", self.id," y mande un ",mensaje," de ",eleccion," al nodo ",destino," en el tiempo", newMessage.getTime())
        self.transmit(newMessage)


    def receive(self, event):
        if(event.getName()=="PARO"):
            self.estadoAnterior = self.estado
            self.estadoParo = True
        
        if(self.estadoParo == False):
            if(self.estado == "NOLIDER"):
                """Sirve para ignorar T2 anterior, cuando entra al HB hace uno nuevo"""
                if(event.getName()=="EXPIRAT2" and self.ignoraTiempo):
                    self.ignoraTiempo = False
                    return
                
                if(event.getName()=="EXPIRAT2"):
                    self.mensajes("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                    self.estado = "ALERTA"
                    return

                print("Estado nolider:Soy el nodo", self.id, "y recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())
                if(event.getName()=="HB"):
                    self.ignoraTiempo = True
                    self.mensajes("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                    self.mensajes("OK", self.clock+1.0, self.banderaLider,self.id,None)
                    print ("Soy el nodo", self.id," y mande un OK al nodo",self.banderaLider," en el tiempo",self.clock)
                    self.estado = "NOLIDER"

                if(event.getName()=="ELECCION"):
                    if(int(event.getElecto())>self.id):
                        self.banderaLider = int(event.getElecto())
                    else:
                        self.banderaLider = self.id
                    for i in self.sinVisitar:
                        self.mensajes("ELECCION", self.clock+1.0,i,self.id,self.banderaLider)
                        print ("Soy el nodo", self.id," y mande un ELECCION de",self.banderaLider," al nodo ",i," en el tiempo",event.getTime()+1 )
                    self.mensajes("EXPIRAT3", self.clock+3.0, self.id,self.id,None)
                    self.estado = "ELECCION"



            elif(self.estado=="ALERTA"):
                print ("Estado alerta:Soy el nodo", self.id, "y recibi un",event.getName(), " en el tiempo",event.getTime(),"del nodo", event.getSource())
                if(event.getName()=="EXPIRAT2"):
                    self.banderaLider = self.id
                    for i in range(len(self.sinVisitar)):
                        self.mensajes("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.banderaLider)
                        print ("Soy el nodo", self.id," y mande un ELECCION de",self.banderaLider," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )
                    self.mensajes("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.estado = "ELECCION"
                if(event.getName() == "ELECCION"):
                    if(event.getElecto()>self.id):
                        self.banderaLider = event.getElecto()
                    else:
                        self.banderaLider = self.id
                    for i in range(len(self.sinVisitar)):
                        self.mensajes("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.banderaLider)
                        print ("Soy el nodo", self.id," y mande un ELECCION de",self.banderaLider," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )
                    
                    self.mensajes("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.estado = "ELECCION"
                if(event.getName()=="HB"):
                    self.ignoraTiempo = True
                    self.mensajes("EXPIRAT2",self.clock+3.0,self.id,self.id,None)
                    self.mensajes("OK",self.clock+1.0,self.banderaLider,self.id,None)
                    self.estado = "NOLIDER"



            elif(self.estado=="ELECCION"):
                if(event.getName()=="HB" or event.getName()=="OK" ):
                    self.estado = "ELECCION"
                    return
                
                if(event.getName()=="ELECCION"):
                    if(event.getElecto()>self.banderaLider):
                        self.banderaLider = event.getElecto()
                    self.estado = "ELECCION"
                    return
                
                print ("Estado ELECCION:Soy el nodo", self.id, "y recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())

                if(event.getName()=="EXPIRAT3"):
                    if(self.banderaLider == self.id):
                        print("\tSOY EL NODO", self.id," SOY EL NUEVO LIDER")
                        self.mensajes("EXPIRAT1",self.clock+2.0,self.id,self.id,None)
                        self.estado = "LIDER"
                    else:
                        self.mensajes("EXPIRAT2",self.clock+3.0,self.id,self.id,None)
                        self.estado = "NOLIDER"
                
            
            elif(self.estado == "LIDER"):
                print ("Estado LIDER:Soy el nodo", self.id, "y recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())
                if(event.getName()=="EXPIRAT1"):
                    self.ok= []
                    for i in range(len(self.sinVisitar)):
                        self.mensajes("HB",self.clock+1.0,self.sinVisitar[i],self.id,None)
                    self.mensajes("EXPIRAT1",self.clock+2.0,self.id,self.id,None)
                    self.estado = "LIDER"

                if(event.getName()=="OK"):
                    self.ok.append(event.getSource())
                
                if(event.getName() == "HB"):
                    if(event.getSource()>self.banderaLider):
                        self.banderaLider = event.getSource()
                    if(self.banderaLider == self.id):
                        print("\tSOY EL NODO", self.id," SOY EL NUEVO LIDER")
                        self.estado = "LIDER"
                        self.mensajes("HB",self.clock+1.0,event.getSource(),self.id,None)
                    else:
                        self.estado = "NOLIDER"
                
                if(event.getName() == "ELECCION"):
                    if(event.getElecto()>self.banderaLider):
                        self.banderaLider = event.getElecto()
                    # else:
                    #     self.banderaLider = self.id
                    for i in range(len(self.sinVisitar)):
                        self.mensajes("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.banderaLider)
                        print ("Soy el nodo", self.id," y mande un ELECCION de",self.banderaLider," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )

                    self.mensajes("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.estado = "ELECCION"    
        elif(self.estadoParo):
            print("\tSOY EL NODO",self.id," ESTOY FUERA DE SERVICIO")
            self.mensajes("EXPIRAT4",self.clock+20.0,self.id,self.id,None)
            self.estadoParo = self.estado
            self.estado = "PARO"
                       
        if(self.estado =="PARO"):
            if(event.getName()=="EXPIRAT4"):
                print("\tSOY EL NODO: ",self.id,"MEACABO DE RECUPERER DE UNA CATALEPSIA",self.estadoParo)
                self.estado = self.estadoAnterior
                self.estadoParo = False

                
       
       
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print ("Please supply a file name")
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 100)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = ChangRoberts()
    experiment.setModel(m, i)
    

#inserta un evento semilla en la agenda y arranca





seed = []
for i in range(1,len(experiment.graph)+1):
    seed.append(EventEleccionFallas("EXPIRAT2",0.0,i,i,0))
    experiment.init(seed[i-1])

seed2 = EventEleccionFallas("PARO", 10.0, 5, 5,0)
experiment.init(seed2)
experiment.run()
