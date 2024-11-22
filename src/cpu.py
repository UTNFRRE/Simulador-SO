from tabulate import tabulate
from colorama import Fore, init

init(autoreset=True)


class cpu:
    
    procesoActual = None
    def __init__(self):
        self.proceso = None
        self.tiempoRestante = 0

    #metodo que asigna un proceso al cpu
    def asignarProceso(self, proceso):
        self.procesoActual = proceso
      
    #metodo que ejecuta un ciclo de reloj 
    def ejecutar(self):
            self.tiempoRestante -= 1
            self.procesoActual.tiempoRestante -= 1
           
    
    def getProcesoActual(self):
        return self.procesoActual
    
    def getTiempoRestante(self):
        return self.tiempoRestante
    
    def setTiempoRestante(self, nuevo_tiempo):
        self.tiempoRestante = nuevo_tiempo

    #metodo que retorna si el cpu esta ocupado
    def estaOcupado(self):
        return self.getProcesoActual() != None
    
    def mostrarCpu(self, tiempo_actual):
        if self.estaOcupado():

            data = [
             [Fore.CYAN + f"{tiempo_actual}" + Fore.RESET, Fore.GREEN + f"{self.getProcesoActual().PID}" + Fore.RESET],
            ]
            headers = ['Tiempo Actual', 'Proceso en ejecucion']
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print("No hay proceso en ejecución")