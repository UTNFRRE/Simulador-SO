#clase proceso
class proceso:
    #constructor
    def __init__(self, PID, TA, TI,tamaño):
        self.PID = PID
        self.tiempoArribo = TA
        self.tiempoIrrupcion = TI
        self.tamaño = tamaño
        self.tiempoRestante = TI
        self.tiempoEspera = 0
        self.tiempoRetorno = 0
        self.particion = 0
        self.estado = "new"

    def __str__(self) -> str:
        pass

    # getter for tamaño
    def get_tamaño(self):
        return self.tamaño

    # setter for tamaño
    def set_tamaño(self, nuevo_tamaño):
        self.tamaño = nuevo_tamaño
    
    # getter for restante
    def get_restante(self):
        return self.restante
    
    # setter for restante
    def set_restante(self, nuevo_restante):
        self.restante = nuevo_restante

    def get_arribo(self):
        return self.tiempoArribo

    # setter for espera
    def set_espera(self, nuevo_espera):
        self.tiempoEspera = nuevo_espera

    #setter for retorno
    def set_retorno(self, nuevo_retorno):
        self.tiempoRetorno = nuevo_retorno

    def set_particion(self, particion):
        self.particion = particion

    def set_estado(self, estado):
        self.estado = estado
        if estado.lower() == "finished":
            self.tiempoEspera = self.tiempoRetorno - self.tiempoIrrupcion
    def get_estado(self):
        return self.estado