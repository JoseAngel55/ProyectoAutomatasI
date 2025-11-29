from lexer import Lexer
from parser import Parser
from symbols import TablaSimbolos
from semantic import AnalizadorSemantico

def evaluar_expresion(expresion):
    if expresion['tipo'] == 'numero':
        return expresion['valor']
    elif expresion['tipo'] == 'string':
        return expresion['valor']
    elif expresion['tipo'] == 'operacion_binaria':
        izquierda = evaluar_expresion(expresion['izquierda'])
        derecha = evaluar_expresion(expresion['derecha'])

        if izquierda is None or derecha is None:
            return None

        if expresion['operador'] == 'SUMA':
            return izquierda + derecha
        elif expresion['operador'] == 'RESTA':
            return izquierda - derecha
        elif expresion['operador'] == 'MULTIPLICACION':
            return izquierda * derecha
        elif expresion['operador'] == 'DIVISION':
            return izquierda / derecha

        return None

def ejecutar(arbol):
    for instruccion in arbol['instrucciones']:
        if instruccion['tipo'] in ['mostrar','decir']:
            resultado = evaluar_expresion(instruccion['valor'])
            if resultado is not None:
                print(resultado)
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