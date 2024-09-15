#Planificador encargado de asignar procesos de disco a memoria

class planificadorMedio:

    def __init__(self, memoria):
        self.memoria = memoria

    #Llamar a worst fit pasando los procesos q esten en disco. Esta bien q worst fit este en el planificador a largo plazo????

    # Se puede hacer una clase abstracta planificadores de memoria y que ahi este el wf
    def planificar_memoria(self, tiempo_actual):
        procesos = self.memoria.getColaListosEnDisco()
        for proceso in procesos:
            if (tiempo_actual >= proceso.get_arribo() and proceso.get_estado() == "inDisk"):   
                self.WorstFit(proceso)