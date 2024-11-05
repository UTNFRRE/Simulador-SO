#logica principal del simulador
from proceso import proceso
from cpu import cpu
from memoria import memoria
from planLargo import planificadorLargo
from planCorto import planificadorCorto
from planMedio import planificadorMedio

import tkinter as tk   #Para usar una ventana para elegir el archivo
from tkinter import filedialog
import os  #Para limpiar la terminal

# falta generar informe
# falta optimizar lo de la carga del archivo
# falta probar el planificador medio


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

    def cargar_procesos(self):
        root = tk.Tk()
        root.withdraw() 

        archivo = filedialog.askopenfilename(title="Seleccionar archivo con los procesos", filetypes=[("Text files", "*.txt")])

        if archivo:
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

    def limpiar_terminal(self):
        if os.name == 'nt':  # Para Windows
            os.system('cls')
        else:  # Para Unix/Linux/MacOS
            os.system('clear')

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
        self.cpu.mostrarCpu() #muestra el estado del cpu
        print("Procesos:")
        for proceso in self.procesos:
             print(f"Proceso {proceso.PID} {proceso.tiempoArribo} {proceso.tiempoIrrupcion} {proceso.tamaño} {proceso.estado}")
        self.memoria.mostrarMemoria() #muestra el estado de la memoria
        input("Presione Enter para continuar...")

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


    def generar_informe(self):
        n = 0
        trTotal = 0
        teTotal = 0
        print("informe estadistico:\n")
        print(" PID\tTiempo de retorno\tTiempo de espera\n")
        for proceso in self.procesos:
            if proceso.get_estado().lower() == "finished":
                n += 1
                trTotal += proceso.tiempoRetorno
                teTotal += proceso.tiempoEspera
                print(f"    {proceso.PID}\t{proceso.tiempoRetorno}\t{proceso.tiempoEspera}\n")
        print(" Tiempo de retorno promedio\tTiempo de espera promedio\n")
        print(f" {round(trTotal/n,2)}\t{round(teTotal/n)}\n")
        print(" Rendimiento del sistema\n")
        print(f"    {round(n/self.tiempo_actual,2)} procesos por unidad de tiempo\n")

# Ejecutar simulación
simulador = Simulador(5,3)
simulador.limpiar_terminal()
simulador.cargar_procesos()
simulador.ejecutar_simulacion()
simulador.generar_informe()
