import base64

# Função para converter imagem em Base64
def imagem_para_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as imagem:
        return base64.b64encode(imagem.read()).decode('utf-8')
