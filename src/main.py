#logica principal del simulador
from proceso import proceso
from cpu import cpu
from memoria import memoria
from planLargo import planificadorLargo

import msvcrt

# por ahi se accede a los atrbutos con get y por ahi con el punto, unificar
# tdv no esta implementado la memoria secundaria, por ahora si un proceso no termina en el quantum se lo saca de memoria
# se podria implementar una lista de procesos terminados
# al hacer cambio de contexto te muestra dos estados pero no suma un ciclo de reloj

class Simulador:
    def __init__(self):
        self.procesos = []
        self.memoria = memoria()
        self.cpu = cpu()
        self.planificadorLargoPlazo = planificadorLargo(self.memoria, self.procesos)
        self.multiprogramacion = 5   #numero de procesos que pueden estar en la cola de listos
        self.tiempo_actual = 0
        self.quantum = 3

    def cargar_procesos(self, archivo):
     with open(archivo, 'r') as f:
        next(f)  # Saltar la primera línea de encabezado
        for linea in f:
            datos = linea.split()
            PID = int(datos[0])
            tamaño = int(datos[1])
            tiempoArribo = int(datos[2])
            tiempoIrrupcion = int(datos[3])
            self.procesos.append(proceso(PID, tiempoArribo, tiempoIrrupcion, tamaño))
     self.planificadorLargoPlazo.set_procesos(self.procesos)

     # self.planificadorLargoPlazo.WorstFit
    

    def planificar_cpu_memoria(self):
            # Mover procesos de la cola de nuevos a la cola de listos si hay espacio
            while len(self.cola_listos) < 5 and self.cola_nuevos:
                proceso = self.cola_nuevos.pop(0)
                if self.asignar_memoria(proceso):
                    self.cola_listos.append(proceso)
        
            # Ejecutar proceso actual en CPU
            if self.cpu.estaOcupado():
                self.cpu.ejecutar(self.tiempo_actual)     #si el cpu esta ocupado se ejecuta un ciclo de reloj y se decrementa el tiempo restante del proceso actual
                proceso_actual = self.cpu.getProcesoActual()
                if (self.cpu.getTiempoRestante() == 0 or proceso_actual.tiempoRestante == 0):  #si el tiempo restante del proceso actual es 0 o el tiempo restante del quantum es 0
                    if proceso_actual.tiempoRestante > 0: 
                        self.cola_listos.append(proceso_actual) #se añade el proceso a la cola de listos
                    else:
                        proceso_actual.tiempoRetorno = self.tiempo_actual - proceso_actual.tiempoArribo
                    self.cpu.setProcesoActual(None)
                    self.memoria.liberarParticion(proceso_actual.particion)  # se libera la partición en cualquier caso
                
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
            print(f"Tiempo restante CPU: {self.cpu.getTiempoRestante()}")
            print(f"Tiempo restante proceso: {self.cpu.getProcesoActual().tiempoRestante}")
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

        input("Presione Enter para continuar o cualquier otra tecla para cancelar...")

    # Método que ejecuta la simulación en un ciclo de reloj
    def ejecutar_simulacion(self):
        while self.procesos or self.cola_listos or self.cola_nuevos or self.cpu.estaOcupado(): #mientras haya procesos en la cola de procesos, en la cola de listos, en la cola de nuevos o el cpu este ocupado
            self.ejecutar_ciclo()

    # Método que ejecuta un ciclo de reloj
    def ejecutar_ciclo(self):
        self.planificar_cpu_memoria()
        self.mostrar_estado()


    # def generar_informe(self):
    #     tiempos_retorno = [proceso.tiempoRetorno for proceso in self.procesos]
    #     tiempos_espera = [proceso.tiempoEspera for proceso in self.procesos]
    #     print("Informe estadístico:")
    #     for proceso in self.procesos:
    #         print(f"Proceso {proceso.PID}: Tiempo de retorno {proceso.tiempoRetorno}, Tiempo de espera {proceso.tiempoEspera}")
    #     print(f"Tiempo promedio de retorno: {sum(tiempos_retorno) / len(tiempos_retorno)}")
    #     print(f"Tiempo promedio de espera: {sum(tiempos_espera) / len(tiempos_espera)}")
    #     print(f"Rendimiento del sistema: {len(self.procesos) / self.tiempo_actual}")

# Ejecutar simulación
simulador = Simulador()
simulador.cargar_procesos('procesos.txt')
simulador.ejecutar_simulacion()
# simulador.generar_informe()
