# Esta clase tiene la responsabilidad de encontrar una particion de memoria para un proceso

class planificadorMemoria:

    def __init__(self, memoria, multiprogramacion):
        self.memoria = memoria
        self.multiprogramacion = multiprogramacion

    def WorstFit(self, proceso):
        particion_elegida = None
        particiones = self.memoria.getParticiones()
        max_fragmentacion = -1
        for particion in particiones:
            if not particion.ocupado and particion.tamaño >= proceso.tamaño:
                fragmentacion = particion.tamaño - proceso.tamaño
                if fragmentacion > max_fragmentacion:
                    max_fragmentacion = fragmentacion
                    particion_elegida = particiones.index(particion)
        if particion_elegida != None:
            self.memoria.añadirProceso(proceso, particion_elegida)    
            return True
        return False

    def GuardarEnDisco(self, proceso):
        self.memoria.AsignarColaListosEnDisco(proceso)             

    def planificar_memoria(self, tiempo_actual):
        pass