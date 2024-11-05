#Esta clase tiene la responsabilidad de asignar cpu a procesos cargados en memoria

class planificadorCorto:

    def __init__(self, memoria, cpu, quantum):
        self.memoria = memoria
        self.colaListos = []
        self.colaTerminados = []
        self.cpu = cpu
        self.quantum = quantum

    def dispatcher(self, tiempo_actual):
        proceso_actual = self.cpu.getProcesoActual()
        if proceso_actual != None:
            if (self.cpu.getTiempoRestante() == 0 or proceso_actual.tiempoRestante == 0):
                if proceso_actual.tiempoRestante > 0: 
                    self.memoria.cola_listos[0].append(proceso_actual) #se añade el proceso a la cola de listos
                    proceso_actual.set_estado("Ready")
                else:
                    self.terminar_proceso(tiempo_actual, proceso_actual)
                self.cpu.asignarProceso(None)
                self.memoria.EliminarColaListosEnMemoria(proceso_actual)


    def terminar_proceso(self, tiempo_actual, proceso_actual):
        proceso_actual.set_retorno( tiempo_actual - proceso_actual.get_arribo() )
        particion_index = self.memoria.getParticionProceso(proceso_actual)
        if particion_index is not None:
            self.memoria.liberarParticion(particion_index)
        self.colaTerminados.append(proceso_actual)
        proceso_actual.set_estado("Finished")


    def planificar_cpu(self, tiempo_actual):
        #Asignar procesos de la cola de listos al CPU
        if not self.cpu.estaOcupado():
            self.colaListos = self.memoria.cola_listos[0]
            if self.colaListos:
                proceso_actual = self.colaListos[0]  # obtener el primer proceso de la cola de listos sin eliminarlo
                self.cpu.asignarProceso(proceso_actual)
                proceso_actual.set_estado("Running")
                self.cpu.setTiempoRestante(self.quantum)
        
        # Ejecutar proceso actual en CPU
        if self.cpu.estaOcupado():
            self.cpu.ejecutar()

                

    def getColaTerminados(self):
        return self.colaTerminados
        

        
