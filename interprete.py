from mi_parser import NodoPrograma
from mi_parser import NodoDeclaracion
from mi_parser import NodoAsignacion
from mi_parser import NodoMostrar
from mi_parser import NodoNumero
from mi_parser import NodoTexto
from mi_parser import NodoVariable
from mi_parser import NodoBinario

import os
class Interprete:
    def __init__(self, tabla_simbolos):
        self.tabla = tabla_simbolos
        self.valores = {}  # Almacena los valores de las variables
    
    def ejecutar(self, programa):
        """Ejecuta el programa completo"""
        if not isinstance(programa, NodoPrograma):
            return
        
        print("\n--- EJECUCIÓN DEL PROGRAMA ---")
        for sentencia in programa.sentencias:
            self.ejecutar_sentencia(sentencia)
    
    def ejecutar_sentencia(self, nodo):
        if isinstance(nodo, NodoDeclaracion):
            # Inicializar variable con valor por defecto
            if nodo.tipo == "entero":
                self.valores[nodo.nombre] = 0
            elif nodo.tipo == "texto":
                self.valores[nodo.nombre] = ""
        
        elif isinstance(nodo, NodoAsignacion):
            # Evaluar expresión y asignar
            valor = self.evaluar_expresion(nodo.expresion)
            self.valores[nodo.nombre] = valor
        
        elif isinstance(nodo, NodoMostrar):
            # Evaluar y mostrar
            valor = self.evaluar_expresion(nodo.expresion)
            print(f">>> {valor}")
    
    def evaluar_expresion(self, nodo):
        if isinstance(nodo, NodoNumero):
            return nodo.valor
        
        elif isinstance(nodo, NodoTexto):
            return nodo.valor
        
        elif isinstance(nodo, NodoVariable):
            return self.valores.get(nodo.nombre, 0)
        
        elif isinstance(nodo, NodoBinario):
            izq = self.evaluar_expresion(nodo.izquierda)
            der = self.evaluar_expresion(nodo.derecha)
            
            if nodo.op == "+":
                return izq + der
            elif nodo.op == "-":
                return izq - der
            elif nodo.op == "*":
                return izq * der
            elif nodo.op == "/":
                return izq // der if isinstance(izq, int) else izq / der
        
        return None