#clase proceso
class proceso:
    #constructor
    restante = 0
    def __init__(self, PID, TI, tamaño):
        self.PID = PID
        self.TI = TI
        self.tamaño = tamaño
        self.restante = TI

    # getter for tamaño
    def get_tamaño(self):
        return self.tamaño

    # setter for tamaño
    def set_tamaño(self, nuevo_tamaño):
        self.tamaño = nuevo_tamaño