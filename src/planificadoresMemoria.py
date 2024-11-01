# clase abtracta planificadores de memoria, incluye planificador largo y medio

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
            self.memoria.añadirProceso(proceso, particion_elegida)    # pedir a memoria q añada, y memoria pide a particion
            # proceso.set_particion(particion_elegida)
            return True
        return False

    def GuardarEnDisco(self, proceso):
            if ((self.memoria.getTamañoCola()) < self.multiprogramacion): 
                self.memoria.AsignarColaListosEnDisco(proceso)
                proceso.set_estado("Ready and suspended")

    def planificar_memoria(self, tiempo_actual):
        pass