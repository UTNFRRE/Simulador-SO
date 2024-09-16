#logica principal del simulador
from proceso import proceso
from cpu import cpu
from memoria import memoria
from planLargo import planificadorLargo
from planCorto import planificadorCorto
from planMedio import planificadorMedio

# se podria implementar una lista de procesos terminados


class Simulador:
    def __init__(self, multiprogramacion, quantum):
        self.procesos = []
        self.memoria = memoria()
        self.cpu = cpu()
        self.multiprogramacion = multiprogramacion   #numero de procesos que pueden estar en la cola de listos
        self.quantum = quantum
        self.planificadorLargoPlazo = planificadorLargo(self.memoria, self.procesos, self.multiprogramacion)
        self.planificadorCortoPlazo = planificadorCorto(self.memoria, self.cpu, self.quantum)
        self.planificadorMedioPlazo = planificadorMedio(self.memoria, self.multiprogramacion)
        self.tiempo_actual = 0

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


    # Asignar Memoria
    def planificar_memoria(self):
        self.planificadorMedioPlazo.planificar_memoria(self.tiempo_actual)
        self.planificadorLargoPlazo.planificar_memoria(self.tiempo_actual)    
        
    # Ejecutar proceso actual en CPU
    def planificar_cpu(self):
        self.planificadorCortoPlazo.planificar_cpu(self.tiempo_actual)

    #Ver como ir liberando memoria
                
    def mostrar_estado(self):
        print(f"Tiempo actual: {self.tiempo_actual}")

        if self.cpu.estaOcupado():
            print(f"Proceso en ejecución: {self.cpu.getProcesoActual().PID}")
            print(f"Tiempo restante CPU: {self.cpu.getTiempoRestante()}")
            print(f"Tiempo restante proceso: {self.cpu.getProcesoActual().tiempoRestante}")
        else:
            print("No hay proceso en ejecución")
        
        print("Procesos:")
        for proceso in self.procesos:
             print(f"Proceso {proceso.tiempoArribo} {proceso.tiempoIrrupcion} {proceso.tamaño} {proceso.estado}")

        print("Tabla de particiones:")
        for particion in self.memoria.getParticiones():
            print(f"Partición {particion.tamaño}K en {particion.dirInicio}K: Proceso {particion.proceso.PID if particion.proceso else 'Ninguno'}, Fragmentación {particion.fragmentacionInterna}K")

        print("Cola de procesos listos:")
        for proceso in self.memoria.cola_listos[0]:
            print(f"Proceso {proceso.PID}")


        input("Presione Enter para continuar o cualquier otra tecla para cancelar...")

    # Método que ejecuta la simulación en un ciclo de reloj
    def ejecutar_simulacion(self):
        while True: #mientras haya procesos en la cola de procesos, en la cola de listos, en la cola de nuevos o el cpu este ocupado
            self.planificadorCortoPlazo.terminar_proceso(self.tiempo_actual)
            if len(self.procesos) == len(self.planificadorCortoPlazo.getColaTerminados()):
                self.mostrar_estado()
                # self.generar_informe()
                break
            self.ejecutar_ciclo()

    # Método que ejecuta un ciclo de reloj
    def ejecutar_ciclo(self):
        self.planificar_memoria()
        self.planificar_cpu()
        self.mostrar_estado()
        self.tiempo_actual += 1


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
simulador = Simulador(5,3)
simulador.cargar_procesos('ejemplo 2.txt')
simulador.ejecutar_simulacion()
# simulador.generar_informe()
