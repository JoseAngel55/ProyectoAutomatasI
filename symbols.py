# Tabla de símbolos para el compilador

class Simbolo:
    """
    Representa una variable en nuestro programa.
    Guarda: nombre, tipo, si fue usada, etc.
    """
    def __init__(self, nombre, tipo, linea=None):
        self.nombre = nombre     
        self.tipo = tipo         
        self.linea = linea       
        self.usada = False        # Si la variable se ha usado en alguna expresión

    def __repr__(self):
        return f"Simbolo({self.nombre}, tipo={self.tipo}, linea={self.linea})"

