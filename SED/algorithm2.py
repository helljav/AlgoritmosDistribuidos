# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion con Retro (Segall) 
como ejemplo de aplicacion """

import sys
from event import Event
from model import Model
from simulation import Simulation

class Algorithm2(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        print "inicializo algoritmo"
        self.visited = False
        self.father = self.id
        self.count = 1

    def receive(self, event):
        """ Aqui se definen las acciones concretas que deben ejecutarse cuando se
        recibe un evento """
        self.count -= 1
        if self.visited == False:
            print "recibo mensaje"
            self.visited = True
            self.father = event.getSource()
            for t in self.neighbors:
                if t != self.father:			
                    newevent = Event("C", self.clock+1.0, t, self.id)
                    self.transmit(newevent)
                    self.count += 1
        if self.count == 0:
            print "termino"
            newevent = Event("C", self.clock+1.0, self.father, self.id)
            self.transmit(newevent)


# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print "Please supply a file name"
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 500)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = Algorithm2()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("C", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
