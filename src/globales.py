
class variablesGlobales:
    _instance = None
    bandera = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(variablesGlobales, cls).__new__(cls, *args, **kwargs)
            cls._instance.bandera = False
        return cls._instance
    
    