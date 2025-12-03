# main.py

from lexer import Lexer
import os

def probar_ejemplos():
    ruta = "ejemplos"

    for archivo in os.listdir(ruta):
        if archivo.endswith(".bz"):
            print(f"\n===== Analizando: {archivo} =====")
            contenido = open(os.path.join(ruta, archivo), "r", encoding="utf-8").read()
            lexer = Lexer(contenido)
            tokens = lexer.analizar()
            for t in tokens:
                print(t)

if __name__ == "__main__":
    probar_ejemplos()
