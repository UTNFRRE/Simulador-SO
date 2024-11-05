#clase planLargo (planificador a latgo plazo)
from planificadoresMemoria import planificadorMemoria

# 1- Worst fit 
# asignar la particion 
# manejar la cola de procesos nuevos

class planificadorLargo(planificadorMemoria):


    def __init__(self, memoria, procesos, multiprogramacion):
        super().__init__(memoria, multiprogramacion)
        self.procesos = procesos
 
    def set_procesos(self, procesos):
        self.procesos = procesos

    def planificar_memoria(self, tiempo_actual):
        for proceso in self.procesos:
            if (tiempo_actual >= proceso.get_arribo() and (proceso.get_estado() == "new")):   
                if self.WorstFit(proceso):
                    proceso.set_estado("Ready")
                else:
                    if ((self.memoria.getTamañoCola()) < self.multiprogramacion):
                        print ("Se guardará el proceso ", proceso.PID, " en disco")
                        self.GuardarEnDisco(proceso)
        

    