class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def declarar(self, nombre, valor, tipo):
        self.simbolos[nombre] = {"valor": valor, "tipo": tipo}

    def obtener(self, nombre):
        return self.simbolos.get(nombre)

    def existe(self, nombre):
        return nombre in self.simbolos