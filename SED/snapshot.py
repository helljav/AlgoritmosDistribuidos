# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation



class chandyLamport(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        self.sinVisitar = self.neighbors[:]
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        self.padre = self.id
        """Variables que son del protocolo"""
        self.bchi = []
        self.mensajesChi = []
        self.chi = [0]*(len(self.neighbors))
        self.banderaSnap = False #"""Esta bandera sirve para saber si aun no le mandan foto por primera vez y ayuda a abrir y cerrar el registro""""
        self.sigma = []
        for i in range(0,len(self.neighbors)):
            self.bchi.append(False)  
        
        print ("inicializo algoritmo")

    
    def goTo(self):
        if(len(self.sinVisitar)!=0):
            k = self.sinVisitar.pop(0)
            newMassage = Event("DESC", self.clock+1.0, k , self.id)
            print ("Soy el nodo", self.id, "y mande un DESC a ", k, "en el tiempo: ", newMassage.getTime())
            self.transmit(newMassage)
        elif(self.padre != self.id):
            newMassage = Event("REG", self.clock+1.0, self.padre , self.id)
            print ("Soy el nodo", self.id, "y mande un REG a ", self.padre, "en el tiempo: ", newMassage.getTime())
            self.transmit(newMassage)
        

    def receive(self, event):
        

        """***************PROTOCOLO SNAPSHOT*********************************************************"""
        if(event.getName() == "FOTO"):
            for i in range(0,len(self.neighbors)):
                if(event.getSource() == self.neighbors[i]):
                    self.bchi[i] = True
            if(self.banderaSnap == False):
                self.banderaSnap = True
                """Guarda el estado local del  nodo en ese momento"""
                self.sigma.append(self.visited)
                self.sigma.append(self.padre)
                self.sigma.append(self.sinVisitar)
                for i in range(0,len(self.neighbors)):
                    if(event.getSource() == self.neighbors[i]):
                        self.bchi[i] = True              
                

                """"Mandan FOTO a todos sus vecinos"""
                for t in self.neighbors: 
                    newMessage = Event("FOTO", self.clock+1.0, t, self.id)
                    #print ("\tSoy el nodo", self.id," y mande FOTO a ",t," en el tiempo", newMessage.getTime())
                    self.transmit(newMessage)

                """Creamos los canales para cada uno de los nodos (chis)"""
                """Cambian el estado de chi dependiendo del origen igual a vacio"""
                if(event.getSource() != self.id):
                    for i in range(0,len(self.neighbors)):
                        if(event.getSource() == self.neighbors[i]):
                            self.chi[i] = event.getSource(),self.id,self.mensajesChi,True
                        else: 
                            self.chi[i] = self.neighbors[i],self.id,None,True
                    
                else:
                    """Este caso es cuando eres una semilla, ya que necesita un arreglo chi mas grande"""
                    self.chi = [0]*(len(self.neighbors)+1)
                    """Creamos su propio canal hasta el ultimo del arreglo"""
                    self.chi[len(self.chi)-1] = event.getSource(),self.id,self.mensajesChi,True
                    for i in range(0,len(self.neighbors)):
                        self.chi[i] = self.neighbors[i],self.id,None,True
                        
                print("    Soy el nodo",self.id, "mi edo local es: ",self.sigma)
                print("    mi estado de canal chi es: ", self.chi)
                print("    Iniciando registro de mensages")
            else:
                
                for i in range(0,len(self.neighbors)):
                    if(event.getSource() == self.neighbors[i]):
                        self.bchi[i] = True
                """Si recibe otro mensaje FOTO por el canal, cierra el registro de ese canal con la bandera de la tupla"""
                for i in range(len(self.chi)):#-1
                    if(event.getSource() == int(self.chi[i][0])):
                        T = self.chi[i]
                        T = list(T)
                        T[3] = False                     
                        T = tuple(T)
                        self.chi[i] = T
                        print("    Soy el nodo",self.id," cierro mi registro del canal",self.chi[i][0],self.chi[i][1])
                
                bandera = True
                for i in range(len(self.bchi)):
                    if(self.bchi[i] == False):
                        bandera = False
                        break
                if(bandera == True):
                    """Si todos sus canales le mandan FOTO, da por terminado el protocolo SNAP"""
                    self.banderaSnap = False
                    for i in range(len(self.chi)):
                        print("    Mensajes : ",self.chi[i][0],self.id,self.chi[i][2])
                    
         
        """****************************************CIDON**********************************************"""



        #identificar si el mensaje recibido es un aviso
        if(event.getName()=="AVISO"):
            """Protocolo snap"""
            if(self.banderaSnap==True):
                for i in range(len(self.chi)):
                    if(event.getSource() == self.chi[i][0] and self.chi[i][1] == self.id):
                        if(self.chi[i][3] == True):
                            T = self.chi[i]
                            T = list(T)
                            if(T[2] == None):
                                arreglo1 = []
                                T[2] = arreglo1
                            T[2].append("AVISO")                        
                            T = tuple(T)
                            self.chi[i] = T                      

            """Cidon"""                       
            if (event.getSource() in self.sinVisitar):                
                self.sinVisitar.remove(event.getSource())
            
        
        elif(event.getName() == "DESC"):
            """Protocolo snap"""
            if(self.banderaSnap==True):
                for i in range(len(self.chi)):
                    if(event.getSource() == self.chi[i][0] and self.chi[i][1] == self.id):
                        if(self.chi[i][3] == True):
                            T = self.chi[i]
                            T = list(T)
                            if(T[2] == None):
                                arreglo2 = []
                                T[2] = arreglo2
                            T[2].append("DESC")                        
                            T = tuple(T)
                            self.chi[i] = T

            """Cidon"""
            #Enviar el aviso a sus vecinos
            for t in self.neighbors: 
                newMessage = Event("AVISO", self.clock+1.0, t, self.id)
                print ("Soy el nodo", self.id," y mande un AVISO a ",t," en el tiempo", newMessage.getTime())
                self.transmit(newMessage)
                
            if (event.getSource() in self.sinVisitar):                
                self.sinVisitar.remove(event.getSource())       
            self.visited = True
            self.padre = event.getSource()        
            self.goTo()                


        elif(event.getName() == "REG"):
            """Protocolo snap"""
            if(self.banderaSnap==True):
                for i in range(len(self.chi)):
                    if(event.getSource() == self.chi[i][0] and self.chi[i][1] == self.id):
                        if(self.chi[i][3] == True):
                            T = self.chi[i]
                            T = list(T)
                            if(T[2] == None):
                                arreglo3 = []
                                T[2] = arreglo3
                            T[2].append("REG")                        
                            T = tuple(T)
                            self.chi[i] = T
            self.goTo()
        #print("\t\t\t",event.getSource(),self.id,self.mensajesChi) 



       
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
    m = chandyLamport()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("DESC", 0.0, 1, 1)
#semilla de snapshot
snap = Event("FOTO",0.9,3,3)
experiment.init(seed)
experiment.init(snap)
experiment.run()
