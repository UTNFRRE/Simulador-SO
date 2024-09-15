#Esta clase tiene la responsabilidad de asignar cpu a procesos cargados en memoria

class PlanificadorCorto:

    def __init__(self, memoria, cpu, quantum):
        self.memoria = memoria
        self.colaListos = []
        self.cpu = cpu
        self.quantum = quantum

    def planificar_cpu(self):
        #Asignar procesos de la cola de listos al CPU
        if not self.cpu.estaOcupado():
            self.colaListos = self.memoria.cola_listos
            if self.colaListos[0]:
                proceso_actual = self.colaListos[0].pop(0)  #se elige el primer proceso de la cola de listos
                self.cpu.asignarProceso(proceso_actual)
                self.cpu.setTiempoRestante(self.quantum)

        # Ejecutar proceso actual en CPU
        self.cpu.ejecutar()     
        proceso_actual = self.cpu.getProcesoActual()
        if (self.cpu.getTiempoRestante() == 0 or proceso_actual.tiempoRestante == 0):
            if proceso_actual.tiempoRestante > 0: 
                self.cola_listos.append(proceso_actual) #se añade el proceso a la cola de listos
            else:
                proceso_actual.tiempoRetorno = self.tiempo_actual - proceso_actual.tiempoArribo
            self.cpu.asignarProceso(None)

        
