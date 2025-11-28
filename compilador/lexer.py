class Token:
    def __init__(self, tipo, valor, linea=None):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, {repr(self.valor)})"

class Lexer:
    #Es un diccionario que establece las palabras reservadas del sistema
    PALABRAS_RESERVADAS = {
        'mostrar': 'MOSTRAR',
        'decir': 'DECIR',
        'numero': 'NUMERO'
    }

    #Constructor del lexer
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea_actual = 1
        self.caracter_actual = self.texto[self.pos] if self.texto else None

    #Manejo de errores
    def error(self):
        raise Exception(f'Carácter inválido en línea {self.linea_actual}')

    #Avanzar un carácter (Mueve el “cursor” una posición a la derecha.
    #Si ya no hay más caracteres (se pasó del final), pone caracter_actual = None, que significa fin del texto.)
    def avanzar(self):
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caracter_actual = None
        else:
            self.caracter_actual = self.texto[self.pos]

    #Saltar espacios en blanco
    def saltar_espacios(self):
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.avanzar()

    #Leer un string (texto entre comillas)
    def string(self):
        resultado = ''
        self.avanzar()
        while self.caracter_actual is not None and self.caracter_actual != '"':
            resultado += self.caracter_actual
            self.avanzar()
        self.avanzar()
        return resultado

    #Leer un identificador (o palabra reservada)
    def identificador(self):
        resultado = ''
        while self.caracter_actual is not None and (self.caracter_actual.isalnum() or self.caracter_actual == '_'):
            resultado += self.caracter_actual
            self.avanzar()
        return resultado
    
    #Leer un numero (Numeros enteros)
    def numero(self):
        resultado = ''
        while self.caracter_actual is not None and self.caracter_actual.isdigit():
            resultado += self.caracter_actual
            self.avanzar()
        return int(resultado)

    def obtener_siguiente_token(self):
        while self.caracter_actual is not None:
            if self.caracter_actual.isspace():
                self.saltar_espacios()
                continue

            if self.caracter_actual == '"':
                return Token('STRING', self.string(), self.linea_actual)
            
            if self.caracter_actual.isdigit():
                valor = self.numero()
                return Token('NUMERO', valor, self.linea_actual)
            
            if self.caracter_actual.isalpha():
                id_text = self.identificador()
                if id_text in self.PALABRAS_RESERVADAS:
                    return Token(self.PALABRAS_RESERVADAS[id_text], id_text, self.linea_actual)
                else:
                    return Token('IDENTIFICADOR', id_text, self.linea_actual)

            self.error()

        return Token('EOF', None, self.linea_actual)