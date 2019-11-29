# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation



class VectorClock(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        self.sinVisitar = self.neighbors[:]
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        self.padre = self.id
        self.reloj = [0]*3
        self.contadorId = 0
        
        print ("inicializo algoritmo")

    
    def goTo(self,event):
        if(len(self.sinVisitar)!=0):
            self.reloj = event.getReloj()[:]
            self.contadorId += 1
            self.reloj[self.id-1] = self.contadorId            
            k = self.sinVisitar.pop(0)
            newMassage = Event("DESC", self.clock+1.0, k , self.id,self.reloj)
            print ("Soy el nodo", self.id, "y mande un DESC a ", k, "en el tiempo: ", newMassage.getTime(),"Selle el mensaje con: ", self.reloj)
            self.transmit(newMassage)
        elif(self.padre != self.id):
            self.reloj = event.getReloj()[:]
            self.contadorId += 1
            self.reloj[self.id-1] = self.contadorId            
            newMassage = Event("REG", self.clock+1.0, self.padre , self.id,self.reloj)
            print ("Soy el nodo", self.id, "y mande un REG a ", self.padre, "en el tiempo: ", newMassage.getTime(),"Selle el mensaje con: ", self.reloj)
            self.transmit(newMassage)
        

    def receive(self, event):
        if(event.getName()=="REG"):
            self.reloj = event.getReloj()[:]
            self.contadorId += 1
            self.reloj[self.id-1] = self.contadorId
            print("Soy el nodo",self.id, "Recibi el mensaje REG con nuevo sello", self.reloj)
         
        #identificar si el mensaje recibido es un aviso
        if(event.getName()=="AVISO"):
            self.reloj = event.getReloj()[:]
            self.contadorId += 1
            self.reloj[self.id-1] = self.contadorId
            print("Soy el nodo",self.id, "Recibi el mensaje AVISO con nuevo sello", self.reloj)
            if (event.getSource() in self.sinVisitar):                
                self.sinVisitar.remove(event.getSource())
            
        
        elif(event.getName() == "DESC"):

            self.reloj = event.getReloj()[:]
            self.contadorId +=1
            self.reloj[self.id-1] = self.contadorId
            print("Soy el nodo",self.id, "Recibi el mensaje DESC con nuevo sello", self.reloj)
            #Enviar el aviso a sus vecinos
            self.contadorId +=1
            self.reloj[self.id-1] = self.contadorId
            for t in self.neighbors: 
                newMessage = Event("AVISO", self.clock+1.0, t, self.id, self.reloj)
                print ("Soy el nodo", self.id," y mande un AVISO a ",t," en el tiempo", newMessage.getTime(),"Selle el mensaje con: ", self.reloj)
                self.transmit(newMessage)
                
            if (event.getSource() in self.sinVisitar):                
                self.sinVisitar.remove(event.getSource())       
            self.visited = True
            self.padre = event.getSource()        
            self.goTo(event)                
        else:
            if(self.visited == True):
                pass#self.sinVisitar = []
            self.goTo(event) 



       
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
    m = VectorClock()
    experiment.setModel(m, i)
reloj = [0]*3
# inserta un evento semilla en la agenda y arranca
seed = Event("DESC", 0.0, 1, 1,reloj)
experiment.init(seed)
experiment.run()
