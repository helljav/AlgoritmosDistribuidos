# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
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
        self.banderaLider = None
        self.sinVisitar = self.neighbors[:]


    def mensajes(self, destino, remitente,mensaje):
        """ Se manda a llamar cada vez que se quiere enviar un mensaje"""
        newMessage = Event(mensaje, self.clock+1.0, destino, remitente)
        print ("Soy el nodo", self.id," y mande un ",mensaje," de ",remitente," al nodo ",self.sinVisitar[0]," en el tiempo", newMessage.getTime())
        self.transmit(newMessage)


    def receive(self, event):
                
        if(event.getName()=="ELECCION"):
            if(int(event.getSource()) > int(self.id)):
                self.mensajes(self.sinVisitar[0],event.getSource(),"ELECCION")
            else:
                if((int(event.getSource())<= int(self.id)) and self.activo != True):
                    self.mensajes(self.sinVisitar[0],self.id,"ELECCION")
                    self.activo = True
                elif(event.getSource()==self.id):
                    self.mensajes(self.sinVisitar[0],self.id,"LIDER")
                
        
        if(event.getName()=="LIDER"):
            self.banderaLider = event.getSource()
            if(event.getSource() != self.id):
                self.mensajes(self.sinVisitar[0],event.getSource(),"LIDER")
       
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


# seed = Event("ELECCION", 0.0, 8, 8)
# experiment.init(seed)



seed = []
for i in range(1,len(experiment.graph)+1):
    seed.append(Event("ELECCION",0.0,i,i))
    experiment.init(seed[i-1])
experiment.run()
