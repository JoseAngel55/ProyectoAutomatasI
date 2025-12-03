# Tabla de símbolos para el compilador

class Simbolo:
    """
    Representa una variable en nuestro programa.
    Guarda: nombre, tipo, si fue usada, etc.
    """
    def __init__(self, nombre, tipo, linea=None):
        self.nombre = nombre      # Ej: "x", "mensaje"
        self.tipo = tipo          # "entero" o "texto"
        self.linea = linea        # Línea donde se declaró (opcional)
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
    
    def obtener_tipo(self, nombre):
        """
        Obtiene el tipo de una variable (entero o texto).
        Retorna None si no existe.
        """
        simbolo = self.buscar(nombre)
        if simbolo:
            return simbolo.tipo
        return None
    
    def variables_no_usadas(self):
        """
        Retorna una lista de variables declaradas pero nunca usadas.
        Útil para advertencias (warnings).
        """
        return [s for s in self.simbolos.values() if not s.usada]
    
    def error(self, msg):
        """
        Registra un error relacionado con símbolos.
        """
        self.errores.append(f"[Error de Símbolos] {msg}")
    
    def mostrar_tabla(self):
        """
        Imprime toda la tabla de símbolos (útil para debugging).
        """
        print("\n=== TABLA DE SÍMBOLOS ===")
        if not self.simbolos:
            print("(vacía)")
        else:
            for nombre, simbolo in self.simbolos.items():
                usada_str = "✓" if simbolo.usada else "✗"
                print(f"  {nombre:15} | tipo: {simbolo.tipo:10} | usada: {usada_str}")
    
    def mostrar_errores(self):
        """
        Imprime todos los errores encontrados.
        """
        print("\n--- ERRORES DE SÍMBOLOS ---")
        if self.errores:
            for e in self.errores:
                print(e)
        else:
            print("Sin errores de símbolos ✔")