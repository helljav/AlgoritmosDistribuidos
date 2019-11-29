
# Este archivo contiene la implementacion de la clase Event (11.11.10)
""" Un objeto de la clase Event encapsula la informacion que se intercambia 
entre las entidades activas de un sistema distribuido """

# ----------------------------------------------------------------------------------------		
class EventPIFAcotado():
                     # Descendiente de la clase "object" (default)
    """ Atributos: "name", "time", "target" y "source", 
    contiene tambien un constructor y los metodos que devuelven cada
    uno de los atributos individuales """
    
    def __init__(self, name, time, target, source,profundidad):
    
        """ Construye una instancia con los atributos inicializados """
        self.name   = name
        self.time   = time        
        self.target = target        
        self.source = source
        self.profundidad = profundidad
        
		
    def getName(self):
        """ Devuelve el nombre del evento """
        return (self.name)
		
    def getTime(self):
        """ Devuelve el tiempo en el que debe ocurrir el evento """
        return (self.time)
		
    def getTarget(self):
        """ Devuelve la identidad del proceso al que va dirigido """
        return (self.target)
		
    def getSource(self):
        """ Devuelve la identidad del proceso que origina el evento """
        return (self.source)
    def getProfundidad(self):
        """ Devuelve la profundidad del proceso que origina el evento """
        return self.profundidad
        
    
	