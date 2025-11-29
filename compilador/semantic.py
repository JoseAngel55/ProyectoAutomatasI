class AnalizadorSemantico:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos

    def analizar(self, arbol):
        for instruccion in arbol['instrucciones']:
            self.analizar_expresion(instruccion['valor'])
        return True

    def analizar_expresion(self, expresion):
        if expresion['tipo'] == 'numero':
            return 'numero'
        elif expresion['tipo'] == 'string':
            return 'string'
        elif expresion['tipo'] == 'operacion_binaria':
            tipo_izq = self.analizar_expresion(expresion['izquierda'])
            tipo_der = self.analizar_expresion(expresion['derecha'])

            # Permitir operaciones entre mismos tipos
            if tipo_izq == tipo_der:
                return tipo_izq
            else:
                raise Exception(f"Error de tipos: {tipo_izq} y {tipo_der} no son compatibles")

        # Si es otro tipo de expresión, retornar un tipo por defecto
        return 'desconocido'