
from globales import variablesGlobales
from planificadoresMemoria import planificadorMemoria

# Esta clase tiene la responsabilidad de asignar a memoria o disco los procesos nuevos
class planificadorLargo(planificadorMemoria):


    def __init__(self, memoria, procesos, multiprogramacion):
        super().__init__(memoria, multiprogramacion)
        self.procesos = procesos
 
    def set_procesos(self, procesos):
        self.procesos = procesos

    def planificar_memoria(self, tiempo_actual, procesoEnCpu=None):
        for proceso in self.procesos:
            if (tiempo_actual >= proceso.get_arribo() and (proceso.get_estado() == "new")):   
                if self.WorstFit(proceso):
                    variablesGlobales.bandera = True
                    proceso.set_estado("Ready")
                else:
                    # Dependiendo de que si esta libre la cpu o no, es distinta la comparacion para la multiprogramacion
                    if procesoEnCpu is None:
                        if self.memoria.getTamañoCola() < self.multiprogramacion:
                            variablesGlobales.bandera = True
                            self.GuardarEnDisco(proceso)
                            proceso.set_estado("Ready and suspended")
                    else:
                            if (self.memoria.getTamañoCola() + 1) < self.multiprogramacion:
                                variablesGlobales.bandera = True
                                self.GuardarEnDisco(proceso)
                                proceso.set_estado("Ready and suspended")
        

    