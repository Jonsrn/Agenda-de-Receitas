# Aplicativo de Gerenciamento de Receitas

Este aplicativo permite aos usuários criar, visualizar e gerenciar receitas de forma eficiente. Projetado para ser simples e intuitivo, o aplicativo oferece funcionalidades como adicionar novas receitas, visualizar detalhes, e pesquisar receitas por categorias.

*Características*: 

**Cadastro de Receitas**: Usuários podem cadastrar novas receitas com detalhes como nome, tipo (líquido/sólido), categoria (café da manhã, almoço, jantar), tipo de prato (prato principal, aperitivo, sobremesa), país de origem, ingredientes, tempo de preparo e modo de preparo.

**Visualização de Receitas**: As receitas podem ser visualizadas em detalhe, incluindo imagens associadas (quando disponíveis) e bandeiras do país de origem.
Edição e Exclusão: Receitas podem ser facilmente editadas ou excluídas.

**Busca Avançada**: Funcionalidade de busca permite aos usuários encontrar receitas por várias categorias ou diretamente por termos específicos. 

**Tecnologias Utilizadas**:

Python: Linguagem principal para o desenvolvimento do backend.
PyQt5: Usado para criar a interface gráfica do usuário (GUI).
MongoDB: Banco de dados para armazenar informações das receitas.
GridFS: Subsistema do MongoDB para armazenamento de imagens das receitas.
Configuração e Execução

Para executar este aplicativo, siga os passos abaixo:

**Pré-requisitos**
Python 3.x instalado
PyQt5 instalado via pip
MongoDB instalado e rodando localmente ou remotamente
