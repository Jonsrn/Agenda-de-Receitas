class Receita:
    def __init__(self, nome_popular, tipo, categoria, tipo_prato, origem, tempo_preparo, ingredientes, modo_preparo, imagem_id, bandeira_origem_id):
        self.nome_popular = nome_popular
        self.tipo = tipo
        self.categoria = categoria
        self.tipo_prato = tipo_prato
        self.origem = origem
        self.tempo_preparo = tempo_preparo
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.imagem_id = imagem_id
        self.bandeira_origem_id = bandeira_origem_id

    def to_dict(self):
        return {
            "nome_popular": self.nome_popular,
            "tipo": self.tipo,
            "categoria": self.categoria,
            "tipo_prato": self.tipo_prato,
            "origem": self.origem,
            "tempo_preparo": self.tempo_preparo,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "imagem_id": self.imagem_id,
            "bandeira_origem_id": self.bandeira_origem_id
        }
