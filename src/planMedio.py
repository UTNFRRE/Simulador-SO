#Planificador encargado de asignar procesos de disco a memoria
from planificadoresMemoria import planificadorMemoria

class planificadorMedio(planificadorMemoria):

    def __init__(self, memoria, multiprogramacion):
       super().__init__(memoria, multiprogramacion)

    def planificar_memoria(self, tiempo_actual):
        procesos = self.memoria.getColaListosEnDisco()
        for proceso in procesos:  
                if self.WorstFit(proceso):
                    proceso.set_estado("Ready")
                    self.memoria.EliminarColaListosEnDisco(proceso)
        