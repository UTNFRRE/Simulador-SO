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

    def planificar_memoria(self, tiempo_actual, procesoo=None):
        for proceso in self.procesos:
            if (tiempo_actual >= proceso.get_arribo() and (proceso.get_estado() == "new")):   
                if self.WorstFit(proceso):
                    proceso.set_estado("Ready")
                else:
                    print("No hay espacio en memoria para el proceso", )
                    # Dependiendo de que si esta libre la cpu o no, es si debe o no sumar para la multiprogramacion
                    if procesoo is None:
                        if self.memoria.getTamañoCola() < self.multiprogramacion:
                            self.GuardarEnDisco(proceso)
                            proceso.set_estado("Ready and suspended")
                    else:
                            if (self.memoria.getTamañoCola() + 1) < self.multiprogramacion:
                                self.GuardarEnDisco(proceso)
                                proceso.set_estado("Ready and suspended")
        

    