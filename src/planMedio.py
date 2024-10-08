#Planificador encargado de asignar procesos de disco a memoria
from planificadoresMemoria import planificadorMemoria

class planificadorMedio(planificadorMemoria):

    def __init__(self, memoria, multiprogramacion):
       super().__init__(memoria, multiprogramacion)

    def planificar_memoria(self, tiempo_actual):
        procesos = self.memoria.getColaListosEnDisco()
        for proceso in procesos:
            if (tiempo_actual >= proceso.get_arribo() and proceso.get_estado() == "Ready and suspended"):   
                self.WorstFit(proceso)