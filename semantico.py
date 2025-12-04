from mi_parser import *
from symbols import TablaSimbolos, Simbolo

class AnalizadorSemantico:
    def __init__(self):
        self.tabla = TablaSimbolos()
        self.errores = []

    def error(self, msg, linea=None):
        if linea:
            self.errores.append(f"[Error Semántico] Línea {linea}: {msg}")
        else:
            self.errores.append(f"[Error Semántico] {msg}")

    def analizar(self, programa):
        if not isinstance(programa, NodoPrograma):
            self.error("El programa debe ser un NodoPrograma")
            return False

        for sentencia in programa.sentencias:
            self.analizar_sentencia(sentencia)

        variables_no_usadas = self.tabla.variables_no_usadas()
        if variables_no_usadas:
            print("\n--- ADVERTENCIAS ---")
            for var in variables_no_usadas:
                print(f"[Advertencia] Variable '{var.nombre}' declarada pero nunca usada")

        self.tabla.mostrar_tabla()

        return len(self.errores) == 0

    def analizar_sentencia(self, nodo):

        if isinstance(nodo, NodoDeclaracion):
            self.analizar_declaracion(nodo)
        elif isinstance(nodo, NodoAsignacion):
            self.analizar_asignacion(nodo)
        elif isinstance(nodo, NodoMostrar):
            self.analizar_mostrar(nodo)
        elif isinstance(nodo, NodoBinario):
            return self.analizar_expresion(nodo)
        else:
            self.error(f"Tipo de nodo no reconocido: {type(nodo)}")

    def analizar_declaracion(self, nodo):
        # Verificar que el nombre sea válido
        if not nodo.nombre:
            self.error("Nombre de variable inválido")
            return None

        # Agregar a la tabla de símbolos
        self.tabla.agregar(nodo.nombre, nodo.tipo)

    def analizar_asignacion(self, nodo):
        # Verificar que la variable exista
        if not self.tabla.existe(nodo.nombre):
            self.error(f"Variable '{nodo.nombre}' no declarada")
            return None

        # Marcar como usada
        self.tabla.marcar_usada(nodo.nombre)

        # Analizar la expresión
        tipo_expresion = self.analizar_expresion(nodo.expresion)

        # Obtener tipo de la variable
        tipo_variable = self.tabla.obtener_tipo(nodo.nombre)

        # Verificar compatibilidad de tipos
        if tipo_expresion and tipo_variable:
            if tipo_expresion != tipo_variable:
                self.error(f"Tipo incompatible: no se puede asignar '{tipo_expresion}' a variable de tipo '{tipo_variable}'")

        return tipo_expresion

    def analizar_mostrar(self, nodo):
        # Analizar la expresión a mostrar
        tipo = self.analizar_expresion(nodo.expresion)
        return tipo

    def analizar_expresion(self, nodo):
        if isinstance(nodo, NodoNumero):
            return "entero"

        elif isinstance(nodo, NodoTexto):
            return "texto"

        elif isinstance(nodo, NodoVariable):
            # Verificar que la variable exista
            if not self.tabla.existe(nodo.nombre):
                self.error(f"Variable '{nodo.nombre}' no declarada")
                return None

            # Marcar como usada
            self.tabla.marcar_usada(nodo.nombre)

            # Devolver su tipo
            return self.tabla.obtener_tipo(nodo.nombre)

        elif isinstance(nodo, NodoBinario):
            # Analizar lado izquierdo y derecho
            tipo_izq = self.analizar_expresion(nodo.izquierda)
            tipo_der = self.analizar_expresion(nodo.derecha)

            # Verificar compatibilidad de tipos
            if tipo_izq and tipo_der:
                # Operaciones aritméticas solo con enteros
                if nodo.op in ("+", "-", "*", "/"):
                    if tipo_izq != "entero" or tipo_der != "entero":
                        self.error(f"Operación '{nodo.op}' solo válida entre enteros")
                        return None
                    return "entero"

                # Concatenación de textos
                elif nodo.op == "+" and tipo_izq == "texto" and tipo_der == "texto":
                    return "texto"

                else:
                    self.error(f"Operación '{nodo.op}' no válida entre tipos '{tipo_izq}' y '{tipo_der}'")
                    return None

            return None

        self.error(f"Tipo de expresión no reconocida: {type(nodo)}")
        return None

    def mostrar_errores(self):
        print("\n--- ERRORES SEMÁNTICOS ---")
        if self.errores:
            for error in self.errores:
                print(error)
        else:
            print("Sin errores semánticos ✔")

    def obtener_tabla(self):
        return self.tabla