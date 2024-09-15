#logica principal del simulador
from proceso import proceso
from cpu import cpu
from memoria import memoria
from planLargo import planificadorLargo
from planCorto import planificadorCorto

import msvcrt

# por ahi se accede a los atrbutos con get y por ahi con el punto, unificar
# tdv no esta implementado la memoria secundaria, por ahora si un proceso no termina en el quantum se lo saca de memoria
# se podria implementar una lista de procesos terminados
# al hacer cambio de contexto te muestra dos estados pero no suma un ciclo de reloj

class Simulador:
    def __init__(self, multiprogramacion=5, quantum=3):
        self.procesos = []
        self.memoria = memoria()
        self.cpu = cpu()
        self.multiprogramacion = multiprogramacion   #numero de procesos que pueden estar en la cola de listos
        self.quantum = quantum
        self.planificadorLargoPlazo = planificadorLargo(self.memoria, self.procesos)
        self.planificadorCortoPlazo = planificadorCorto(self.memoria, self.cpu, self.quantum)
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

        self.planificadorLargoPlazo.WorstFit()    


    # Planif a mediano plazo. Mover procesos de la cola de nuevos a la cola de listos si hay espacio
    while len(self.cola_listos) < 5 and self.cola_nuevos:
                proceso = self.cola_nuevos.pop(0)
                if self.asignar_memoria(proceso):
                    self.cola_listos.append(proceso)
        
    # Ejecutar proceso actual en CPU
    #Ver como ir liberando memoria
                
    self.tiempo_actual += 1 

            

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
        self.planificar_memoria()
        self.planificar_cpu()
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
