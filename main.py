from lexer import Lexer
from mi_parser import Parser
from mi_parser import NodoPrograma
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

if __name__ == "__main__":
    probar_ejemplos()
