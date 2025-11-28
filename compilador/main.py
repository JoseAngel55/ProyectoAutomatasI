from lexer import Lexer
from parser import Parser
from symbols import TablaSimbolos
from semantic import AnalizadorSemantico

def ejecutar(arbol):
    for instruccion in arbol['instrucciones']:
        if instruccion['tipo'] == 'mostrar':
            print(instruccion['valor'])
        elif instruccion['tipo'] == 'decir':
            print(instruccion['valor'])

def main():

    tabla_simbolos = TablaSimbolos()

    while True:
        try:
            entrada = input("Compilador:) > ").strip()
            if entrada.lower() == 'salir':
                break
            if entrada:
                lexer = Lexer(entrada)
                parser = Parser(lexer)
                arbol = parser.parse()

                analizador = AnalizadorSemantico(tabla_simbolos)
                analizador.analizar(arbol)

                ejecutar(arbol)

        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()