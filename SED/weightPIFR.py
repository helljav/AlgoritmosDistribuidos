# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from eventPesos import EventPesos
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation


class weightPIFR(Model):
    
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        self.padre = self.id # sirve para regresar y reportar al padre
        self.sinVisitar = self.neighbors[:]
        self.recibi = []#Verifica si las aristas ya fueron visitadas
        self.peso = input(f"Dame el el peso para el nodo----> {self.id}   : ") #Peso de cada nodo
        self.pesoMinimo = self.peso
        self.guia = self.id
        for i in range(0,len(self.neighbors)):
            self.recibi.append(False)         
        
        print ("inicializo algoritmo")

   
        
        

    def receive(self, event):       

        if(event.getName()=="INICIO"):
            """ Ponemos la arista correspondiente coo verdadero """
            for i in range(0,len(self.neighbors)):
                if(event.getSource() == self.neighbors[i]):
                    self.recibi[i] = True

            """ Si no ha sido visitada por primera vez manda el mensaje a todos sus vecinos menos el padre"""
            if(self.visited == False):
                self.visited = True
                self.padre = event.getSource() 
                if (event.getSource() in self.sinVisitar):                
                    self.sinVisitar.remove(event.getSource())
                for t in self.sinVisitar: 
                    newMessage = EventPesos("INICIO", self.clock+1.0, t, self.id,None)
                    print ("Soy el nodo", self.id," y mande un INICIO a ",t," en el tiempo", newMessage.getTime())
                    self.transmit(newMessage)

            """" Verifica si todas sus aristas fueron visitados
                    Si todas sus aristas ya fueron visitadas la bandera sera igual a True
            """     
            bandera = True
            for i in range(0,len(self.neighbors)):
                if(self.recibi[i] == False):
                    bandera = False
                    break

            """Si el nodo recibio un inicio y es una hoja, manda un reporte"""
            if(bandera == True):
                if(self.padre != self.id):
                    newMessage = EventPesos("REPORTE", self.clock+1.0, self.padre, self.id,self.peso)
                    print ("Soy el nodo", self.id," y mande un REPORTE a",self.padre," en el tiempo", newMessage.getTime()," con mi peso: ", self.peso)
                    self.transmit(newMessage)

        if(event.getName()=="REPORTE"):
           

            if(self.padre!=self.id):

                """ Ponemos la arista correspondiente como verdadero """
                for i in range(0,len(self.neighbors)):
                    if(event.getSource() == self.neighbors[i]):
                        self.recibi[i] = True

                pesoFuente = int(event.getPeso())
                """ Evalua primero los pesos"""
                if(pesoFuente<int(self.pesoMinimo)):
                    self.pesoMinimo = pesoFuente
                    self.guia = event.getSource()
                
                
                
                print("Soy el nodo",self.id, "comparo peso mandado desde el nodo: ", event.getSource(),"peso minimo escogido:", self.pesoMinimo)

                

                bandera = True
                for i in range(0,len(self.neighbors)):
                    if(self.recibi[i] == False):
                        bandera = False
                        break

                if(bandera == True):
                    """Mando un reporte a mi padre"""
                    newMessage = EventPesos("REPORTE", self.clock+1.0, self.padre, self.id,self.pesoMinimo)
                    print ("Soy el nodo", self.id," y mande un REPORTE a ",self.padre," en el tiempo", newMessage.getTime()," con mi peso: ", self.pesoMinimo)
                    self.transmit(newMessage)
            
            if(self.padre == self.id):
                
                for i in range(0,len(self.neighbors)):
                    if(event.getSource() == self.neighbors[i]):
                        self.recibi[i] = True

               
                if(int(event.getPeso())<int(self.pesoMinimo)):
                    self.pesoMinimo = event.getPeso()
                    self.guia = event.getSource()
                    

                print("Soy el nodo",self.id, "comparo peso mandado desde el nodo: ", event.getSource(),"Peso minimo escogido:", self.pesoMinimo)

                bandera = True
                for i in range(0,len(self.neighbors)):
                    if(self.recibi[i] == False):
                        bandera = False
                        break

                if(bandera == True):
                    """Manda el mensaje cambia desde la semilla"""
                    newMessage = EventPesos("CAMBIA", self.clock+1.0, self.guia, self.id,self.pesoMinimo)
                    print ("Soy el nodo", self.id," y mande un CAMBIA al nodo  ",self.guia," en el tiempo", newMessage.getTime()," Con peso: ", self.pesoMinimo)
                    self.transmit(newMessage)
                

        if(event.getName()=="CAMBIA"):
            if(self.guia==self.id):
                aumenta = int(self.pesoMinimo)+1
                print("Peso minimo encontrado: ",self.pesoMinimo ,"en el nodo",self.id," Aumenta peso: ", aumenta )
            else:
                """Manda el mensaje cambia desde nodos intermedios"""
                newMessage = EventPesos("CAMBIA", self.clock+1.0, self.guia, self.id,self.pesoMinimo)
                print ("Soy el nodo", self.id," y mande un CAMBIA al nodo  ",self.guia," en el tiempo", newMessage.getTime()," Con peso: ", self.pesoMinimo)
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
    m = weightPIFR()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = EventPesos("INICIO", 0.0, 2, 2,0)
experiment.init(seed)
experiment.run()
