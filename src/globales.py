# Esta clase tiene la responsabilidad de guardar variables globales accesibles por todas las clases

# La variable bandera es utilizada para solo mostrar el estado de la simulacion 
# si se ha realizado algun cambio de contexto o se ha asignado un proceso a memoria
class variablesGlobales:
    _instance = None
    bandera = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(variablesGlobales, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    