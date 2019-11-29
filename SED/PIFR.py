# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation


class PIFR(Model):
    
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        self.padre = self.id
        self.sinVisitar = self.neighbors[:]
        self.recibi = []
        
        for i in range(0,len(self.neighbors)):
            self.recibi.append(False)         
        
        print ("inicializo algoritmo")
        

    def receive(self, event):
        if(event.getName()=="M"):
            for i in range(0,len(self.neighbors)):
                if(event.getSource() == self.neighbors[i]):
                    self.recibi[i] = True
            if(self.visited == False):
                self.visited = True
                self.padre = event.getSource() 
                if (event.getSource() in self.sinVisitar):                
                    self.sinVisitar.remove(event.getSource())
                for t in self.sinVisitar: 
                    newMessage = Event("M", self.clock+1.0, t, self.id)
                    print ("Soy el nodo", self.id," y mande un M a ",t," en el tiempo", newMessage.getTime())
                    self.transmit(newMessage)

            bandera = True
            for i in range(0,len(self.neighbors)):
                if(self.recibi[i] == False):
                    bandera = False
                    break
            if(bandera == True):
                if(self.padre != self.id):
                    newMessage = Event("M", self.clock+1.0, self.padre, self.id)
                    print ("Soy el nodo", self.id," y mande un M a ",self.padre," en el tiempo", newMessage.getTime())
                    self.transmit(newMessage)

       



       
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
    m = PIFR()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("M", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
