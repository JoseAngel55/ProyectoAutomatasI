from lexer import Lexer
import os

def probar_ejemplos():
    ruta = "ejemplos"

    for archivo in os.listdir(ruta):
        if archivo.endswith(".bz"):
            print(f"\n===== Analizando: {archivo} =====")

            contenido = open(os.path.join(ruta, archivo), "r", encoding="utf-8").read()
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

if __name__ == "__main__":
    probar_ejemplos()
