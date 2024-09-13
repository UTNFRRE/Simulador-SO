#logica principal del simulador
from proceso import proceso
from cpu import cpu
from memoria import memoria

# por ahi se accede a los atrbutos con get y por ahi con el punto, unificar
# tdv no esta implementado la memoria secundaria
# se podria implementar una lista de procesos terminados

class Simulador:
    def __init__(self):
        self.procesos = []
        self.memoria = memoria()
        self.cpu = cpu()
        self.cola_listos = []
        self.cola_nuevos = []
        self.multiprogramacion = 5   #numero de procesos que pueden estar en la cola de listos
        self.tiempo_actual = 1
        self.quantum = 3

    def cargar_procesos(self, archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                PID, TA, TI, tamaño = map(int, linea.split())
                self.procesos.append(proceso(PID, TA, TI, tamaño))

    def asignar_memoria(self, proceso):    #por cada particion calcula la fragmentacion interna y elige la particion con mayor fragmentacion
        particion_elegida = None
        max_fragmentacion = -1
        for particion in self.memoria.getParticiones():
            if not particion.ocupado and particion.tamaño >= proceso.tamaño:
                fragmentacion = particion.tamaño - proceso.tamaño
                if fragmentacion > max_fragmentacion:
                    max_fragmentacion = fragmentacion
                    particion_elegida = particion
        if particion_elegida:
            particion_elegida.añadir_proceso(proceso)
            return True
        return False

    def planificar_cpu_memoria(self):
            # Cargar procesos que han llegado
            for proceso in self.procesos[:]:    #por cada proceso en la lista de procesos
                if proceso.tiempoArribo <= self.tiempo_actual:  # si el tiempo de arribo del proceso es menor o igual al tiempo actual se intenta asignar memoria
                    if len(self.cola_listos) < self.multiprogramacion:  #si la cola de listos no esta llena
                        if self.asignar_memoria(proceso):  #si se asigna memoria se añade a la cola de listos y se elimina de la lista de procesos
                            self.cola_listos.append(proceso)   # agregar proceso a la cola de listos
                    else:
                        self.cola_nuevos.append(proceso)  #si la cola de listos esta llena se añade a la cola de nuevos
                    self.procesos.remove(proceso)  #se asigna a una de las colas y se elimina el proceso de la lista de procesos

            # Mover procesos de la cola de nuevos a la cola de listos si hay espacio
            while len(self.cola_listos) < 5 and self.cola_nuevos:
                proceso = self.cola_nuevos.pop(0)
                if self.asignar_memoria(proceso):
                    self.cola_listos.append(proceso)
        
            # Ejecutar proceso actual en CPU
            if self.cpu.estaOcupado():
                self.cpu.ejecutar(self.tiempo_actual)     #si el cpu esta ocupado se ejecuta un ciclo de reloj y se decrementa el tiempo restante del proceso actual
                if self.cpu.getTiempoRestante() == 0 or self.cpu.getProcesoActual().tiempoRestante == 0:  #si el tiempo restante del proceso actual es 0 o el tiempo restante del quantum es 0
                    if self.cpu.getProcesoActual().tiempoRestante > 0: 
                        self.cola_listos.append(self.cpu.getProcesoActual()) #se añade el proceso a la cola de listos
                    self.memoria.liberarParticion(self.cpu.getProcesoActual().PID) #se libera la particion
                
                self.tiempo_actual += 1 # solo se aumenta el tiempo actual si el cpu esta ocupado

            else:     #si el cpu no esta ocupado asigna un proceso de la cola de listos al cpu
                if self.cola_listos:    #si hay procesos en la cola de listos, elige el primero y lo asigna al cpu
                    proceso_actual = self.cola_listos.pop(0)
                    self.cpu.asignarProceso(proceso_actual)
                    self.cpu.setTiempoRestante(self.quantum)

            

    def mostrar_estado(self):
        print(f"Tiempo actual: {self.tiempo_actual}")

        if self.cpu.estaOcupado():
            print(f"Proceso en ejecución: {self.cpu.getProcesoActual().PID}")
        else:
            print("No hay proceso en ejecución")

        print("Tabla de particiones:")
        for particion in self.memoria.getParticiones():
            print(f"Partición {particion.tamaño}K en {particion.dirInicio}K: Proceso {particion.proceso.PID if particion.proceso else 'Ninguno'}, Fragmentación {particion.fragmentacionInterna}K")

        print("Cola de procesos listos:")
        for proceso in self.cola_listos:
            print(f"Proceso {proceso.PID}")

        print("Cola de nuevos procesos:")
        for proceso in self.cola_nuevos:
            print(f"Proceso {proceso.PID}")

    # Método que ejecuta la simulación en un ciclo de reloj
    def ejecutar_simulacion(self):
        while self.procesos or self.cola_listos or self.cola_nuevos or self.cpu.estaOcupado(): #mientras haya procesos en la cola de procesos, en la cola de listos, en la cola de nuevos o el cpu este ocupado
            self.ejecutar_ciclo()

    # Método que ejecuta un ciclo de reloj
    def ejecutar_ciclo(self):
        self.planificar_cpu_memoria()
        self.mostrar_estado()

    def generar_informe(self):
        tiempos_retorno = [proceso.tiempoRetorno for proceso in self.procesos]
        tiempos_espera = [proceso.tiempoEspera for proceso in self.procesos]
        print("Informe estadístico:")
        for proceso in self.procesos:
            print(f"Proceso {proceso.PID}: Tiempo de retorno {proceso.tiempoRetorno}, Tiempo de espera {proceso.tiempoEspera}")
        print(f"Tiempo promedio de retorno: {sum(tiempos_retorno) / len(tiempos_retorno)}")
        print(f"Tiempo promedio de espera: {sum(tiempos_espera) / len(tiempos_espera)}")
        print(f"Rendimiento del sistema: {len(self.procesos) / self.tiempo_actual}")

# Ejemplo de uso
simulador = Simulador()
simulador.cargar_procesos('procesos.txt')
simulador.ejecutar_simulacion()
simulador.generar_informe()
