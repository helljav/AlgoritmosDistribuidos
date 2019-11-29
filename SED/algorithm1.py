# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class Algorithm1(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        print "inicializo algoritmo"

    def receive(self, event):
        """ Aqui se definen las acciones concretas que deben ejecutarse cuando se
        recibe un evento """
        if self.visited == False:
            print "soy ", self.id, " recibo mensaje a las ", self.clock, " desde ", event.getSource()
            self.visited = True
            for t in self.neighbors: 
                newevent = Event("C", self.clock+1.0, t, self.id)
                print " proximo evento a las ", newevent.getTime()
                self.transmit(newevent)


# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print "Please supply a file name"
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 100)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = Algorithm1()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("C", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
