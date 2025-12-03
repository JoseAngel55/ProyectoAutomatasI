from lexer import Token;

class NodoPrograma:
    def __init__(self, sentencias):
        self.sentencias = sentencias

    def __repr__(self):
        return f"Programa({self.sentencias})"

class NodoDeclaracion:
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

    def __repr__(self):
        return f"Declaracion({self.tipo}, {self.nombre})"

class NodoAsignacion:
    def __init__(self, nombre, expresion):
        self.nombre = nombre
        self.expresion = expresion

    def __repr__(self):
        return f"Asignacion({self.nombre}, {self.expresion})"

class NodoMostrar:
    def __init__(self, expresion):
        self.expresion = expresion

    def __repr__(self):
        return f"Mostrar({self.expresion})"

class NodoBinario:
    def __init__(self, op, izquierda, derecha):
        self.op = op
        self.izquierda = izquierda
        self.derecha = derecha
    
    def __repr__(self):
        return f"Binario({self.op}, {self.izquierda}, {self.derecha})"

class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Numero({self.valor})"

class NodoTexto:
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Texto({self.valor})"

class NodoVariable:
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Variable({self.nombre})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def avanzar(self):
        self.pos += 1
    
    def error(self, msg):
        self.errores.append(f"[Error Sintáctico] Pos {self.pos}: {msg} ")
    
    def consumirToken(self, tipo, valor=None):
        tok = self.actual()
        if tok is not None and tok.tipo == tipo and (valor is None or tok.valor == valor):
            self.avanzar()
            return tok

        esperado = tipo if valor is None else f"{tipo}('{valor}')"
        encontrado = "EOF" if tok is None else f"{tok.tipo}('{tok.valor}')"
        self.error(f"Se esperaba {esperado} pero se encontró {encontrado} ")
        return None

    #descartar tokens hasta encontrar ";"
    def sincronizar(self):
        while self.actual() is not None and self.actual().tipo != "PUNTO_Y_COMA":
            self.avanzar()
        if self.actual() is not None and self.actual().tipo == "PUNTO_Y_COMA":
            self.avanzar()

    def parse(self):
        sentencias = []
        while self.actual() is not None:
            tok = self.actual()
            
            if tok.tipo in ("TIPO_ENTERO", "TIPO_TEXTO"):
                nodo = self.declaracion()
                if nodo:
                    sentencias.append(nodo)
            elif tok.tipo == "IDENTIFICADOR":
                nodo = self.asignacion()
                if nodo:
                    sentencias.append(nodo)
            elif tok.tipo == "MOSTRAR":
                nodo = self.mostrar()
                if nodo:
                    sentencias.append(nodo)
            else:
                self.error(f"Token inesperado '{tok.valor}' al inicio de una sentencia ")
                self.sincronizar()
                continue
            
        return NodoPrograma(sentencias)
    
    #gramatica libre de contexto
    def declaracion(self):
        # (TIPO ENTERO | TIPO TEXTO) IDENTEIFICADOR PUNTO_Y_COMA
        tipo_tok = self.actual()
        self.avanzar()

        if tipo_tok.tipo == "TIPO_ENTERO":
            tipo = "entero" 
        elif tipo_tok.tipo == "TIPO_TEXTO":
            tipo = "texto"
        else:
            tipo = "desconocido"
        
        ident = self.consumirToken("IDENTIFICADOR")
        self.consumirToken("PUNTO_Y_COMA")
        if ident is None:
            return None
        return NodoDeclaracion(tipo, ident.valor)
    
    def asignacion(self):
        # IDENTIFICADOR = expresion PUNTO_Y_COMA
        ident = self.consumirToken("IDENTIFICADOR")
        self.consumirToken("OP", "=")
        expr = self.expresion()
        self.consumirToken("PUNTO_Y_COMA")
        if ident is None or expr is None:
            return None
        return NodoAsignacion(ident.valor, expr)
    
    def mostrar(self):
        # MOSTRAR expresion PUNTO_Y_COMA
        self.consumirToken("MOSTRAR")
        expr = self.expresion()
        self.consumirToken("PUNTO_Y_COMA")
        if expr is None:
            return None
        return NodoMostrar(expr)
    
    #expresiones
    def expresion(self):
        # expresion --- termino ((+|-|*|/) termino)*
        nodo = self.termino()
        while (self.actual() is not None and self.actual().tipo == "OP" and self.actual().valor in ("+", "-")):
            op_tok = self.actual()
            self.avanzar()
            derecha = self.termino()
            nodo = NodoBinario(op_tok.valor, nodo, derecha)
        return nodo
    
    def termino(self):
        # termino --- factor ((*|/) factor)*
        nodo = self.factor()
        while (self.actual() is not None and self.actual().tipo == "OP" and self.actual().valor in ("*", "/")):
            op_tok = self.actual()
            self.avanzar()
            derecha = self.factor()
            nodo = NodoBinario(op_tok.valor, nodo, derecha)
        return nodo
    
    def factor(self):
        # factor --- NUMERO | TEXTO | IDENTIFICADOR | (expresion)
        tok = self.actual()
        if tok is None:
            self.error("Se esperaba un factor pero se encontro EOF ")
            return None

        if tok.tipo == "NUMERO":
            self.avanzar()
            return NodoNumero(int(tok.valor))
        
        if tok.tipo == "TEXTO":
            self.avanzar()
            return NodoTexto(tok.valor)
        
        if tok.tipo == "IDENTIFICADOR":
            self.avanzar()
            return NodoVariable(tok.valor)
        
        if tok.tipo == "PAREN" and tok.valor == "(":
            self.avanzar()
            nodo = self.expresion()
            self.consumirToken("PAREN", ")")
            return nodo
        
        self.error(f"Factor inesperado '{tok.valor}' ")
        self.avanzar()
        return None
     
            
