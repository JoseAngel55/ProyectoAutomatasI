import string

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"<{self.tipo}: {self.valor}>"

RESERVADAS = {
    "MOSTRAR": "MOSTRAR",
    "CAPTURAR": "CAPTURAR",
    "entero": "TIPO_ENTERO",
    "texto": "TIPO_TEXTO",
}

class Lexer:

    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.tokens = []

    def avanzar(self):
        self.pos += 1
        return self.pos < len(self.codigo)

    def caracter_actual(self):
        if self.pos < len(self.codigo):
            return self.codigo[self.pos]
        return None

    def analizar(self):

        while self.pos < len(self.codigo):
            c = self.caracter_actual()

            # Ignorar espacios y saltos
            if c in [" ", "\n", "\t", "\r"]:
                self.pos += 1
                continue

            if c.isdigit():
                numero = ""
                while self.caracter_actual() and self.caracter_actual().isdigit():
                    numero += self.caracter_actual()
                    self.pos += 1
                self.tokens.append(Token("NUMERO", numero))
                continue

            if c.isalpha():
                ident = ""
                while self.caracter_actual() and (self.caracter_actual().isalnum() or self.caracter_actual() == "_"):
                    ident += self.caracter_actual()
                    self.pos += 1

                # Verificar si es reservada
                if ident in RESERVADAS:
                    self.tokens.append(Token(RESERVADAS[ident], ident))
                else:
                    self.tokens.append(Token("IDENTIFICADOR", ident))
                continue

            if c == '"':
                self.pos += 1
                cadena = ""
                while self.caracter_actual() != '"' and self.caracter_actual() is not None:
                    cadena += self.caracter_actual()
                    self.pos += 1

                # Cerrar comilla
                if self.caracter_actual() == '"':
                    self.pos += 1
                    self.tokens.append(Token("TEXTO", cadena))
                else:
                    raise Exception("Error léxico: cadena sin cerrar")
                continue

            if c in "+-*/=":
                self.tokens.append(Token("OP", c))
                self.pos += 1
                continue

            if c == ";":
                self.tokens.append(Token("PUNTO_Y_COMA", ";"))
                self.pos += 1
                continue

            raise Exception(f"Error léxico: carácter desconocido '{c}' en posición {self.pos}")

        return self.tokens
