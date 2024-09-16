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
            proceso.set_estado("inMemory")
            return True
        else:
            if ((self.memoria.getTamañoCola() + 1) < self.multiprogramacion):   #se suma 1 por el proceso que esta en cpu
                self.memoria.AsignarColaListosEnDisco(proceso)
                proceso.set_estado("inDisk")
        return False

    def planificar_memoria(self, tiempo_actual):
        pass