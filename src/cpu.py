#clase cpu
class cpu:
    #constructor
    procesoActual = None
    def __init__(self):
        self.proceso = None
        self.tiempoRestante = 0
    #metodo que asigna un proceso al cpu
    def asignarProceso(self, proceso):
        self.procesoActual = proceso
       # self.tiempoRestante = proceso.tiempo  
       # el tiempo restante es el quantum 
    #metodo que ejecuta un ciclo de reloj 
    def ejecutar(self):
        #si hay un proceso en ejecucion se decrementa el tiempo restante de cpu y del proceso actual
            self.tiempoRestante -= 1
            self.procesoActual.tiempoRestante -= 1
            # if self.procesoActual.tiempoEspera == 0:    #hay q ver que pasa con los procesos q se asignan al inicio
            #     self.procesoActual.tiempoEspera = tiempo_actual - self.procesoActual.tiempoArribo
            # if self.tiempoRestante == 0 or self.procesoActual.tiempoRestante == 0:  #si el tiempo restante del proceso actual es 0 o el tiempo restante del quantum es 0
            #     self.procesoActual.tiempoRetorno = tiempo_actual - self.procesoActual.tiempoArribo
            #     self.procesoActual = None     #si el tiempo restante es 0 se libera el cpu
    #metodo que retorna el proceso actual
    def getProcesoActual(self):
        return self.procesoActual
    #metodo que retorna el tiempo restante
    def getTiempoRestante(self):
        return self.tiempoRestante
    # setter del tiempo restante
    def setTiempoRestante(self, nuevo_tiempo):
        self.tiempoRestante = nuevo_tiempo
    #metodo que retorna si el cpu esta ocupado
    def estaOcupado(self):
        return self.getProcesoActual() != None