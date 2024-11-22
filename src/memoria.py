from proceso import proceso
from tabulate import tabulate
from colorama import Fore, init

init(autoreset=True)

class particion:
    proceso = None
    fragmentacionInterna =0
    ocupado = False
    tamaño = 0
    dirInicio = 0

    def __str__(self) -> str:
        pass
    # Permite asignar un proceso a la particion
    def añadir_proceso(self, proceso):
        self.proceso = proceso
        self.ocupado = True
        self.fragmentacionInterna = self.tamaño - proceso.tamaño
    # Permite liberar la particion
    def liberar(self):
        self.proceso = None
        self.ocupado = False
        self.fragmentacionInterna = 0 
    
#Jerarquia de clases para las particiones
class particionGrande(particion):
    tamaño = 250
    dirInicio = 100000
    def _str__(self) -> str:
        return "Particion grande"
class particionMediana(particion):
    tamaño = 150
    dirInicio = 350000
    def _str__(self) -> str:
        return "Particion mediana"
class particionPequeña(particion):
    tamaño = 50
    dirInicio = 500000
    def _str__(self) -> str:
        return "Particion pequeña"

class memoria:
    def __init__(self ):
        self.particiones = [
            particionGrande(),
            particionMediana(),
            particionPequeña()
        ]
        self.cola_listos = [[],[]]   #cola de listos en memoria, listos en disco
        
    def añadirProceso(self, proceso, particion):
        self.particiones[particion].añadir_proceso(proceso)
        self.AsignarColaListosEnMemoria(proceso)
   
    def liberarParticion(self, particion_index):
        self.particiones[particion_index].liberar() 

    def getParticiones(self):
        return self.particiones
    
    # Metodo que retorna la particion en la que se encuentra un proceso
    def getParticionProceso(self, proceso):
        for index, particion in enumerate(self.particiones):
            if particion.proceso == proceso:
                return index
        return None
    
    def AsignarColaListosEnMemoria (self, proceso):
        self.cola_listos[0].append(proceso)

    def AsignarColaListosEnDisco (self, proceso):
        self.cola_listos[1].append(proceso)   

    def EliminarColaListosEnMemoria (self, proceso):
        self.cola_listos[0].remove(proceso)

    def EliminarColaListosEnDisco (self, proceso):
        self.cola_listos[1].remove(proceso)
    
    def getColaListosEnDisco(self):
        return self.cola_listos[1]
    
    def getTamañoCola(self):
        return len(self.cola_listos[0]) + len(self.cola_listos[1])
    
    def mostrarMemoria(self):

        headers = ['Partición','Dirrecion de Inicio', 'Estado','Proceso', 'Fragmentación interna']
        print("Tabla de particiones:")
        data=[]	
        for particion in self.getParticiones():
            particion_info = [f"{particion.tamaño}K",f"{hex(particion.dirInicio)}", Fore.RED + 'Ocupado' + Fore.RESET if particion.proceso else Fore.GREEN + 'Libre' + Fore.RESET, particion.proceso.PID if particion.proceso else '-', f"{particion.fragmentacionInterna}K"]
            data.append(particion_info)
        print(tabulate(data, headers=headers, tablefmt='grid'))

        headers = ['PID', 'Tiempo de Arribo', 'Tamaño', 'Tiempo Restante', 'Cargado en']
        data = []
        if self.cola_listos[0]:
            for proceso in self.cola_listos[0]:
                data.append([proceso.PID, proceso.tiempoArribo, f"{proceso.tamaño}K", proceso.tiempoRestante,Fore.MAGENTA +  "Memoria" + Fore.RESET])
            
        if self.cola_listos[1]:
            for proceso in self.cola_listos[1]:
                data.append([proceso.PID, proceso.tiempoArribo, f"{proceso.tamaño}K", proceso.tiempoRestante,Fore.BLUE +  "Disco" + Fore.RESET])  
        
        if data:
            print("Cola de procesos listos:")
            print(tabulate(data, headers=headers, tablefmt='grid'))