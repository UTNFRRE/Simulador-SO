
#logica principal del simulador
from globales import variablesGlobales
from proceso import proceso
from cpu import cpu
from memoria import memoria
from planLargo import planificadorLargo
from planCorto import planificadorCorto
from planMedio import planificadorMedio


import tkinter as tk   #Para usar una ventana para elegir el archivo
from tkinter import filedialog
import os  #Para limpiar la terminal

#Para mostrar los datos en forma de tabla
from tabulate import tabulate
from colorama import Fore, init
import csv


init(autoreset=True)
# Bandera para saber si mostrar el estado del simulador


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

        archivo = filedialog.askopenfilename(title="Seleccionar archivo con los procesos", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])

        if archivo:
            extension = os.path.splitext(archivo)[1]
            with open(archivo, 'r') as f:
                if extension == '.csv':
                    reader = csv.reader(f)
                    next(reader)  # Saltar la primera línea de encabezado
                    for linea in reader:
                        PID, tamaño, tiempoArribo, tiempoIrrupcion = map(int, linea)
                        self.procesos.append(proceso(PID, tiempoArribo, tiempoIrrupcion, tamaño))
                else:
                    next(f)  # Saltar la primera línea de encabezado
                    for linea in f:
                        datos = linea.split()
                        PID = int(datos[0])
                        tamaño = int(datos[1])
                        tiempoArribo = int(datos[2])
                        tiempoIrrupcion = int(datos[3])
                        self.procesos.append(proceso(PID, tiempoArribo, tiempoIrrupcion, tamaño))
            # Ordenar los procesos por tiempoArribo de menor a mayor
            self.procesos.sort(key=lambda p: p.tiempoArribo)
            self.planificadorLargoPlazo.set_procesos(self.procesos)

    def limpiar_terminal(self):
        if os.name == 'nt':  # Para Windows
            os.system('cls')
        else:  # Para Unix/Linux/MacOS
            os.system('clear')

    # Asignar Memoria
    def planificar_memoria(self):
        self.planificadorMedioPlazo.planificar_memoria(self.tiempo_actual)
        proceso_actual = self.cpu.getProcesoActual()
        self.planificadorLargoPlazo.planificar_memoria(self.tiempo_actual, proceso_actual)
        
    # Ejecutar proceso actual en CPU
    def planificar_cpu(self):
        self.planificadorCortoPlazo.planificar_cpu(self.tiempo_actual)
                
    def mostrar_estado(self):
        
        self.cpu.mostrarCpu(self.tiempo_actual) #muestra el estado del cpu

        self.memoria.mostrarMemoria() #muestra el estado de la memoria

        colaTerminados = self.planificadorCortoPlazo.getColaTerminados()
        headers = []
        if colaTerminados:
            print("Procesos terminados:")
            for proceso in colaTerminados:
                headers.append(Fore.YELLOW + f"{proceso.PID}" + Fore.RESET)
            print(tabulate([headers], tablefmt='grid'))

            
        input("Presione Enter para continuar...")

    # Método que ejecuta la simulación en un ciclo de reloj
    def ejecutar_simulacion(self):
        while True: 
            self.planificadorCortoPlazo.dispatcher(self.tiempo_actual)    #para hacer el cambio de contexto de ser necesario
            if len(self.procesos) == len(self.planificadorCortoPlazo.getColaTerminados()):
                break
            self.ejecutar_ciclo()

    # Método que ejecuta un ciclo de reloj
    def ejecutar_ciclo(self):
        self.planificar_memoria()
        self.planificar_cpu()  
        if variablesGlobales.bandera:
            self.mostrar_estado()
            variablesGlobales.bandera = False
        self.tiempo_actual += 1


    def generar_informe(self):
        n = 0
        trTotal = 0
        teTotal = 0
        print(Fore.GREEN + "Informe estadistico" + Fore.RESET)
        headers = ['PID', 'Tiempo de Retorno', 'Tiempo de Espera']
        data = []
        for proceso in self.procesos:
            if proceso.get_estado().lower() == "finished":
                n += 1
                trTotal += proceso.tiempoRetorno
                teTotal += proceso.tiempoEspera
                data.append([proceso.PID, proceso.tiempoRetorno, proceso.tiempoEspera])
        print(tabulate(data, headers=headers, tablefmt='grid'))
        headers = ['Tiempo de retorno promedio', 'Tiempo de espera promedio', 'Rendimiento del sistema', 'Procesos procesados']
        data = [[round(trTotal/n,2), round(teTotal/n, 2), round(n/self.tiempo_actual,2), n]]
        print(tabulate(data, headers=headers, tablefmt='grid'))

# Ejecutar simulación
simulador = Simulador(5,3)
simulador.limpiar_terminal()
simulador.cargar_procesos()
simulador.ejecutar_simulacion()
simulador.generar_informe()
