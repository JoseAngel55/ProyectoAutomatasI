from lexer import Lexer
from mi_parser import Parser
from semantico import AnalizadorSemantico
from mi_parser import NodoPrograma
from interprete import Interprete
import os

def probar_ejemplos():
    ruta = "ejemplos"

    for archivo in os.listdir(ruta):
        if archivo.endswith(".bz"):
            print(f"\n===== Analizando: {archivo} =====")

            with open(os.path.join(ruta, archivo), "r", encoding="utf-8") as f:
                contenido = f.read()
            
            # análisis léxico
            lexer = Lexer(contenido)
            tokens, errores = lexer.analizar()

            print("\n--- TOKENS ---")
            for t in tokens:
                print(t)

            print("\n--- ERRORES LÉXICOS ---")
            if errores:
                for e in errores:
                    print(e)
            else:
                print("Sin errores léxicos ✔")

            if errores:
                print("Saltando análisis sintáctico/semántico por errores léxicos")
                continue
            
            # analisis sintactico
            parser = Parser(tokens)        
            ast= parser.parse()
            errores_sintacticos = parser.errores

            print("\n--- ARBOL SINTACTICO (AST) ---")
            for nodo in ast.sentencias:
                print(nodo)

            print("\n--- ERRORES SINTACTICOS ---")
            if errores_sintacticos:
                for e in errores_sintacticos:
                    print(e)
            else:
                print("Sin errores sintacticos ✔")

            if errores_sintacticos:
                print("Saltando análisis semántico por errores sintácticos")
                continue

            print("\n--- ANÁLISIS SEMÁNTICO ---")
            analizador = AnalizadorSemantico()
            resultado = analizador.analizar(ast)

            analizador.mostrar_errores()

            if resultado:
                print("\n--- EJECUCIÓN ---")
                interprete = Interprete(analizador.tabla)
                interprete.ejecutar(ast)

                print("COMPILACIÓN EXITOSA")
            else:
                print("COMPILACIÓN FALLIDA (errores semánticos)")

if __name__ == "__main__":
    probar_ejemplos()
