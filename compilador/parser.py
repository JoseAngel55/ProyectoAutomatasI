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
        self.siguiente_token()  # Saltar 'mostrar'
        expresion = self.parse_expresion()
        return {'tipo': 'mostrar', 'valor': expresion}

    def parse_decir(self):
        self.siguiente_token()  # Saltar 'decir'
        expresion = self.parse_expresion()
        return {'tipo': 'decir', 'valor': expresion}

    def parse_expresion(self):
        return self.parse_termino()

    def parse_termino(self):
        nodo = self.parse_factor()

        while self.token_actual.tipo in ['SUMA', 'RESTA']:
            tipo_operador = self.token_actual.tipo
            self.siguiente_token()
            nodo = {
                'tipo': 'operacion_binaria',
                'operador': tipo_operador,
                'izquierda': nodo,
                'derecha': self.parse_factor()
            }

        return nodo

    def parse_factor(self):
        nodo = self.parse_primario()

        while self.token_actual.tipo in ['MULTIPLICACION', 'DIVISION']:
            tipo_operador = self.token_actual.tipo
            self.siguiente_token()
            nodo = {
                'tipo': 'operacion_binaria',
                'operador': tipo_operador,
                'izquierda': nodo,
                'derecha': self.parse_primario()
            }

        return nodo

    def parse_primario(self):
        token = self.token_actual

        if token.tipo == 'NUMERO':
            self.siguiente_token()
            return {'tipo': 'numero', 'valor': token.valor}
        elif token.tipo == 'STRING':
            self.siguiente_token()
            return {'tipo': 'string', 'valor': token.valor}
        else:
            self.error(f"Se esperaba número o string, se obtuvo {token.tipo}")