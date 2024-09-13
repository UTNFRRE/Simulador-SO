from proceso import proceso
# 

class particion:
    proceso = None
    fragmentacionInterna =0
    tiempoAcumulado = 0     #??
    ocupado = False
    tamaño = 0
    dirInicio = 0

    def __str__(self) -> str:
        pass

    #clases para añadir y liberar un proceso a una particion
    def añadir_proceso(self, proceso):
        self.proceso = proceso
        self.ocupado = True
        self.fragmentacionInterna = self.tamaño - proceso.tamaño

    def liberar(self):
        self.proceso = None
        self.ocupado = False
        self.fragmentacionInterna = 0  
    
#la siguiente jerarquia de clases permite que al liberarse una particion
#se pueda saber que tipo de particion es.
class particionGrande(particion):
    tamaño = 250
    dirInicio = 100
    def _str__(self) -> str:
        return "Particion grande"
class particionMediana(particion):
    tamaño = 150
    dirInicio = 350
    def _str__(self) -> str:
        return "Particion mediana"
class particionPequeña(particion):
    tamaño = 50
    dirInicio = 500
    def _str__(self) -> str:
        return "Particion pequeña"
#clase memoria
class memoria:
    def __init__(self):
        self.particiones = [
            particionGrande(),
            particionMediana(),
            particionPequeña()
        ]
    #metodo encargado de añadir un proceso a una particion especifica
    def añadirProceso(self, proceso, particion):
        self.particiones[particion].añadir_proceso(proceso)
    #metodo encargado de liberar una particion, llama al metodo liberar de la clase particion
    def liberarParticion(self, particion):   
        self.particiones[particion].liberar()
    #en cada ciclo de reloj se aumenta el tiempo acumulado de cada particion
    def aumentarTiempo(self):
        for particion in self.particiones:
            if particion.ocupado:
                particion.tiempoAcumulado += 1   

    def getParticiones(self):
        return self.particiones