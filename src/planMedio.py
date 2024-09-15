#Planificador encargado de asignar procesos de disco a memoria

class planificadorMedio:

    def __init__(self, memoria):
        self.memoria = memoria

    #Llamar a worst fit pasando los procesos q esten en disco. Esta bien????