#clase planLargo (planificador a latgo plazo)


# 1- Worst fit 
# asignar la particion 
# manejar la cola de procesos nuevos

class PlanificadorLargo:


    def __init__(self, memoria, procesos):
        self.memoria = memoria
        self.procesos = procesos
        self.cola_nuevos = []
        self.cola_listos = []

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
        if particion_elegida:
            self.memoria.añadirProceso(proceso, particion_elegida)    # pedir a memoria q añada, y memoria pide a particion
            proceso.set_particion(particion_elegida)
            return True
        return False