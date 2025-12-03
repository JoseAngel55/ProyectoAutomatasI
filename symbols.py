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

class TablaSimbolos:
    """
    Administra todos los símbolos (variables) del programa.
    Permite agregar, buscar y validar variables.
    """
    
    def __init__(self):
        # Diccionario: nombre_variable -> objeto Simbolo
        self.simbolos = {}
        self.errores = []
    
    def agregar(self, nombre, tipo, linea=None):
        """
        Agrega una nueva variable a la tabla.
        Si ya existe, reporta un error.
        """
        if nombre in self.simbolos:
            self.error(f"Variable '{nombre}' ya fue declarada anteriormente en línea {self.simbolos[nombre].linea}")
            return False
        
        # Crear el símbolo y agregarlo
        simbolo = Simbolo(nombre, tipo, linea)
        self.simbolos[nombre] = simbolo
        return True
    
    def buscar(self, nombre):
        """
        Busca una variable en la tabla.
        Retorna el objeto Simbolo si existe, None si no.
        """
        return self.simbolos.get(nombre, None)
    
    def existe(self, nombre):
        """
        Verifica si una variable ya fue declarada.
        """
        return nombre in self.simbolos
    
    def marcar_usada(self, nombre):
        """
        Marca una variable como 'usada' cuando aparece en una expresión.
        """
        if nombre in self.simbolos:
            self.simbolos[nombre].usada = True
    

        """
        Imprime todos los errores encontrados.
        """
        print("\n--- ERRORES DE SÍMBOLOS ---")
        if self.errores:
            for e in self.errores:
                print(e)
        else:
            print("Sin errores de símbolos ✔")