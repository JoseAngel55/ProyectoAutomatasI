class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_actual = None
        self.siguiente_token()

    def error(self, mensaje):
        raise Exception(f'Error de sintaxis: {mensaje}')

    def siguiente_token(self):
        self.token_actual = self.lexer.obtener_siguiente_token()

    def parse(self):
        instrucciones = []

        while self.token_actual.tipo != 'EOF':
            if self.token_actual.tipo == 'MOSTRAR':
                instrucciones.append(self.parse_mostrar())
            elif self.token_actual.tipo == 'DECIR':
                instrucciones.append(self.parse_decir())
            else:
                self.error(f"Instrucción no reconocida: {self.token_actual.valor}")

        return {'tipo': 'programa', 'instrucciones': instrucciones}

    def parse_mostrar(self):
        self.siguiente_token()

        if self.token_actual.tipo == 'STRING':
            valor = self.token_actual.valor
            self.siguiente_token()
            return {'tipo': 'mostrar', 'valor': valor}
        else:
            self.error("Se esperaba un string después de 'mostrar'")

    def parse_decir(self):
        self.siguiente_token()

        if self.token_actual.tipo == 'STRING':
            valor = self.token_actual.valor
            self.siguiente_token()
            return {'tipo': 'decir', 'valor': valor}
        else:
            self.error("Se esperaba un string después de 'decir'")