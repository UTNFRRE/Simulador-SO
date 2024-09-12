#clase cpu
class cpu:
    #constructor
    def __init__(self):
        self.proceso = None
        self.tiempoRestante = 0
    #metodo que asigna un proceso al cpu
    def asignarProceso(self, proceso):
        self.procesoActual = proceso
        self.tiempoRestante = proceso.tiempo
    #metodo que ejecuta un ciclo de reloj
    def ejecutar(self):
        if self.procesoActual != None:
            self.tiempoRestante -= 1
            if self.tiempoRestante == 0:
                self.procesoActual = None
        else:
            print("CPU: No hay proceso en ejecucion")
    #metodo que retorna el proceso actual
    def getProcesoActual(self):
        return self.procesoActual
    #metodo que retorna el tiempo restante
    def getTiempoRestante(self):
        return self.tiempoRestante
    #metodo que retorna si el cpu esta ocupado
    def estaOcupado(self):
        return self.procesoActual != None