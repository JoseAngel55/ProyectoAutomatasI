class AnalizadorSemantico:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos

    def analizar(self, arbol):
        for instruccion in arbol['instrucciones']:
            if instruccion['tipo'] in ['mostrar', 'decir']:
                if not isinstance(instruccion['valor'], str):
                    raise Exception(f"Error semántico: se esperaba un string")

        return True