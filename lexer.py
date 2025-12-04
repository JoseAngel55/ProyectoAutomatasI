class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"<{self.tipo}: {self.valor}>"

RESERVADAS = {
    "MOSTRAR": "MOSTRAR",
    "entero": "TIPO_ENTERO",
    "texto": "TIPO_TEXTO",
}

class Lexer:

    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.tokens = []
        self.errores = []

    def avanzar(self):
        self.pos += 1

    def caracter(self):
        if self.pos < len(self.codigo):
            return self.codigo[self.pos]
        return None

    def error(self, msg):
        self.errores.append(f"[Error Léxico] Pos {self.pos}: {msg}")

    def analizar(self):

        while self.pos < len(self.codigo):
            c = self.caracter()

            # Espacios
            if c in " \n\r\t":
                self.avanzar()
                continue

            # Números
            if c.isdigit():
                num = ""
                while self.caracter() and self.caracter().isdigit():
                    num += self.caracter()
                    self.avanzar()
                self.tokens.append(Token("NUMERO", num))
                continue

            # Identificadores y reservadas
            if c.isalpha():
                ident = ""
                while self.caracter() and (self.caracter().isalnum() or self.caracter() == "_"):
                    ident += self.caracter()
                    self.avanzar()

                if ident in RESERVADAS:
                    self.tokens.append(Token(RESERVADAS[ident], ident))
                else:
                    self.tokens.append(Token("IDENTIFICADOR", ident))
                continue

            # Cadenas entre comillas
            if c == '"':
                self.avanzar()
                cadena = ""
                cerrado = False

                while self.caracter() is not None:
                    actual = self.caracter()

                    if actual == '"':
                        cerrado = True
                        self.avanzar()
                        self.tokens.append(Token("TEXTO", cadena))
                        break

                    if actual == "\n":
                        break

                    cadena += actual
                    self.avanzar()

                if not cerrado:
                    self.error("Cadena sin cerrar con comillas")
                    while self.caracter() not in [None, "\n"]:
                        self.avanzar()

                continue

            # Operadores
            if c in "+-*/=":
                self.tokens.append(Token("OP", c))
                self.avanzar()
                continue

            # Punto y coma
            if c == ";":
                self.tokens.append(Token("PUNTO_Y_COMA", ";"))
                self.avanzar()
                continue

            # Símbolo ilegal
            self.error(f"Símbolo inválido '{c}'")
            self.avanzar()

        return self.tokens, self.errores
