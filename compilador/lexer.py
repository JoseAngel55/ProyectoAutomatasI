class Token:
    def __init__(self, tipo, valor, linea=None):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, {repr(self.valor)})"

class Lexer:
    PALABRAS_RESERVADAS = {
        'mostrar': 'MOSTRAR',
        'decir': 'DECIR',
    }

    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea_actual = 1
        self.caracter_actual = self.texto[self.pos] if self.texto else None

    def error(self):
        raise Exception(f'Carácter inválido en línea {self.linea_actual}')

    def avanzar(self):
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caracter_actual = None
        else:
            self.caracter_actual = self.texto[self.pos]

    def saltar_espacios(self):
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.avanzar()

    def string(self):
        resultado = ''
        self.avanzar()
        while self.caracter_actual is not None and self.caracter_actual != '"':
            resultado += self.caracter_actual
            self.avanzar()
        self.avanzar()
        return resultado

    def identificador(self):
        resultado = ''
        while self.caracter_actual is not None and (self.caracter_actual.isalnum() or self.caracter_actual == '_'):
            resultado += self.caracter_actual
            self.avanzar()
        return resultado

    def obtener_siguiente_token(self):
        while self.caracter_actual is not None:
            if self.caracter_actual.isspace():
                self.saltar_espacios()
                continue

            if self.caracter_actual == '"':
                return Token('STRING', self.string(), self.linea_actual)

            if self.caracter_actual.isalpha():
                id_text = self.identificador()
                if id_text in self.PALABRAS_RESERVADAS:
                    return Token(self.PALABRAS_RESERVADAS[id_text], id_text, self.linea_actual)
                else:
                    return Token('IDENTIFICADOR', id_text, self.linea_actual)

            self.error()

        return Token('EOF', None, self.linea_actual)