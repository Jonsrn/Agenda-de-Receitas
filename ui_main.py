from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QPushButton, QLabel, 
    QComboBox, QLineEdit, QDialog, QFileDialog, QListWidget, QListWidgetItem, 
    QFormLayout, QSpinBox, QHBoxLayout, QGridLayout, QFrame, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from db import db, fs
from models import Receita


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicação de Receitas")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.initUI()

    def initUI(self):
        self.home_screen()
        self.insert_screen_step1()
        self.insert_screen_step2()
        self.insert_screen_step3()
        self.query_screen()
        self.advanced_options_screen()

    def add_back_button(self, layout, index_to_go_back=-1):
        back_button = QPushButton("Voltar")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(index_to_go_back if index_to_go_back != -1 else 0))
        layout.addWidget(back_button)    

    def home_screen(self):
        home_widget = QWidget()
        layout = QVBoxLayout()

        # Caminhos das imagens
        insert_image_path = 'escrevendo_receita.jpg'  # Atualize com o caminho correto
        query_image_path = 'consultar.jpg'    # Atualize com o caminho correto

        # Configuração da imagem e botão de inserção
        insert_image_label = QLabel()
        insert_image_pixmap = QPixmap(insert_image_path)
        insert_image_label.setPixmap(insert_image_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        insert_image_label.setAlignment(Qt.AlignCenter)  # Centraliza apenas a imagem
        insert_button = QPushButton("Inserir Receita")
        insert_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Configuração da imagem e botão de consulta
        query_image_label = QLabel()
        query_image_pixmap = QPixmap(query_image_path)
        query_image_label.setPixmap(query_image_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        query_image_label.setAlignment(Qt.AlignCenter)  # Centraliza apenas a imagem
        query_button = QPushButton("Consultar Receita")
        query_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        # Adicionando ao layout principal
        layout.addWidget(insert_image_label)
        layout.addWidget(insert_button)
        layout.addWidget(query_image_label)
        layout.addWidget(query_button)
        advanced_options_button = QPushButton("Opções Avançadas")
        advanced_options_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))  # Índice 5 para opções avançadas
        layout.addWidget(advanced_options_button)

        home_widget.setLayout(layout)
        self.stacked_widget.addWidget(home_widget)
    
    def advanced_options_screen(self):
        advanced_widget = QWidget()
        layout = QVBoxLayout()

        # Imagem e botão para Editar Receita
        edit_image_path = 'editar.jpg'  # Atualize com o caminho correto
        edit_image_label = QLabel()
        edit_image_pixmap = QPixmap(edit_image_path)
        edit_image_label.setPixmap(edit_image_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        edit_image_label.setAlignment(Qt.AlignCenter)
        edit_button = QPushButton("Editar Receita")
        edit_button.clicked.connect(self.edit_recipe)  # Função para editar receitas

        # Imagem e botão para Excluir Receita
        delete_image_path = 'excluir.jpg'  # Atualize com o caminho correto
        delete_image_label = QLabel()
        delete_image_pixmap = QPixmap(delete_image_path)
        delete_image_label.setPixmap(delete_image_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        delete_image_label.setAlignment(Qt.AlignCenter)
        delete_button = QPushButton("Excluir Receita")
        delete_button.clicked.connect(self.delete_recipe)  # Função para excluir receitas

        # Adicionando elementos ao layout
        layout.addWidget(edit_image_label)
        layout.addWidget(edit_button)
        layout.addWidget(delete_image_label)
        layout.addWidget(delete_button)
        self.add_back_button(layout)  # Botão para voltar ao menu principal

        advanced_widget.setLayout(layout)
        self.stacked_widget.addWidget(advanced_widget) 

    def edit_recipe(self):
        dialog = QDialog(self)  # Passar 'self' centraliza em relação à janela principal
        dialog.setWindowTitle("Editar Receita")  # Nome para a caixa de diálogo
        layout = QVBoxLayout()
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Digite o nome da receita para filtrar...")
        recipe_list = QComboBox()
        search_edit.textChanged.connect(lambda: self.filter_recipes(recipe_list, search_edit.text()))

        layout.addWidget(QLabel("Filtrar Receita:"))
        layout.addWidget(search_edit)
        layout.addWidget(QLabel("Selecione a receita para editar:"))
        layout.addWidget(recipe_list)

        button_edit = QPushButton("Editar")
        button_edit.clicked.connect(lambda: self.show_edit_recipe_form(recipe_list.currentData()))
        layout.addWidget(button_edit)

        dialog.setLayout(layout)
        dialog.exec_()

    def filter_recipes(self, combo_box, text):
        combo_box.clear()
        recipes = db.receitas.find({'nome_popular': {'$regex': text, '$options': 'i'}})
        for recipe in recipes:
            combo_box.addItem(recipe['nome_popular'], recipe)

    def show_edit_recipe_form(self, recipe):
        # Formulário de edição
        if recipe is None:
            return
        edit_dialog = QDialog()
        layout = QVBoxLayout()

        nome_edit = QLineEdit(recipe['nome_popular'])
        tempo_preparo_spin = QSpinBox()
        tempo_preparo_spin.setValue(recipe['tempo_preparo'])

        # Adicionar mais campos conforme necessário

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(nome_edit)
        layout.addWidget(QLabel("Tempo de Preparo (minutos):"))
        layout.addWidget(tempo_preparo_spin)

        save_button = QPushButton("Salvar Alterações")
        save_button.clicked.connect(lambda: self.update_recipe(recipe['_id'], nome_edit.text(), tempo_preparo_spin.value()))
        layout.addWidget(save_button)

        edit_dialog.setLayout(layout)
        edit_dialog.exec_()

    def update_recipe(self, recipe_id, nome, tempo_preparo):
        # Atualizar a receita no banco de dados
        db.receitas.update_one({'_id': recipe_id}, {'$set': {'nome_popular': nome, 'tempo_preparo': tempo_preparo}})
        QMessageBox.information(self, "Atualizado", "Receita atualizada com sucesso!")

    def delete_recipe(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Excluir Receita")
        layout = QVBoxLayout()

        # Campo para buscar e filtrar receitas
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Digite o nome da receita para filtrar...")
        recipe_list = QComboBox()
        search_edit.textChanged.connect(lambda: self.filter_recipes(recipe_list, search_edit.text()))

        # Preencher lista de receitas inicialmente
        self.populate_recipe_list(recipe_list)

        layout.addWidget(QLabel("Filtrar Receita:"))
        layout.addWidget(search_edit)
        layout.addWidget(QLabel("Selecione a receita para excluir:"))
        layout.addWidget(recipe_list)

        button_delete = QPushButton("Excluir")
        button_delete.clicked.connect(lambda: self.confirm_deletion(recipe_list.currentData()))
        layout.addWidget(button_delete)

        dialog.setLayout(layout)
        dialog.exec_()

    def populate_recipe_list(self, combo_box):
        combo_box.clear()
        recipes = db.receitas.find()
        for recipe in recipes:
            combo_box.addItem(recipe['nome_popular'], recipe)

    def filter_recipes(self, combo_box, text):
        combo_box.clear()
        recipes = db.receitas.find({'nome_popular': {'$regex': text, '$options': 'i'}})
        for recipe in recipes:
            combo_box.addItem(recipe['nome_popular'], recipe)

    def confirm_deletion(self, recipe):
        if recipe is None:
            return
        # Configurando a caixa de diálogo de confirmação com botões em português
        message_box = QMessageBox(self)
        message_box.setWindowTitle('Confirmar Exclusão')
        message_box.setText('Você tem certeza que deseja excluir esta receita?')
        message_box.setIcon(QMessageBox.Question)
        message_box.addButton('Sim', QMessageBox.YesRole)  # Definindo botão "Sim"
        message_box.addButton('Não', QMessageBox.NoRole)   # Definindo botão "Não"
        reply = message_box.exec_()  # Executando a caixa de diálogo

        if reply == 0:  # O índice 0 corresponde ao botão "Sim" porque foi adicionado primeiro
            db.receitas.delete_one({'_id': recipe['_id']})
            QMessageBox.information(self, "Excluído", "Receita excluída com sucesso!", QMessageBox.Ok)

    
        

    def insert_screen_step1(self):
        insert_step1_widget = QWidget()
        layout = QVBoxLayout()

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Líquido", "Sólido"])
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Café da manhã", "Almoço", "Jantar"])
        self.tipo_prato_combo = QComboBox()
        self.tipo_prato_combo.addItems(["Prato principal", "Aperitivo", "Sobremesa"])

        self.origem_combo = QComboBox()
        self.populate_country_combobox(self.origem_combo)

        layout.addWidget(QLabel("Tipo:"))
        layout.addWidget(self.tipo_combo)
        layout.addWidget(QLabel("Categoria:"))
        layout.addWidget(self.categoria_combo)
        layout.addWidget(QLabel("Tipo de Prato:"))
        layout.addWidget(self.tipo_prato_combo)
        layout.addWidget(QLabel("País de Origem:"))
        layout.addWidget(self.origem_combo)

        next_button = QPushButton("Próximo")
        next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(next_button)
        insert_step1_widget.setLayout(layout)

        self.stacked_widget.addWidget(insert_step1_widget)
        self.add_back_button(layout)

    def insert_screen_step2(self):
        insert_step2_widget = QWidget()
        layout = QVBoxLayout()

        self.nome_popular_edit = QLineEdit()
        self.tempo_preparo_spin = QSpinBox()
        self.tempo_preparo_spin.setMaximum(1440)

        self.ingredientes_layout = QVBoxLayout()
        add_ingrediente_button = QPushButton("+ Adicionar Ingrediente")
        add_ingrediente_button.clicked.connect(self.add_ingrediente_field)

        layout.addWidget(QLabel("Nome Popular:"))
        layout.addWidget(self.nome_popular_edit)
        layout.addWidget(QLabel("Tempo de Preparo (minutos):"))
        layout.addWidget(self.tempo_preparo_spin)
        layout.addWidget(QLabel("Ingredientes:"))
        layout.addLayout(self.ingredientes_layout)
        layout.addWidget(add_ingrediente_button)

        next_button = QPushButton("Próximo")
        next_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        layout.addWidget(next_button)
        insert_step2_widget.setLayout(layout)

        self.stacked_widget.addWidget(insert_step2_widget)
        self.add_back_button(layout, 1)

    def add_ingrediente_field(self):
        ingrediente_widget = QWidget()
        layout = QHBoxLayout()

        nome_edit = QLineEdit()
        quantidade_spin = QSpinBox()
        quantidade_spin.setMaximum(10000)
        unidade_combo = QComboBox()
        unidade_combo.addItems(["gramas", "ml", "unidades"])

        layout.addWidget(nome_edit)
        layout.addWidget(quantidade_spin)
        layout.addWidget(unidade_combo)
        ingrediente_widget.setLayout(layout)
        self.ingredientes_layout.addWidget(ingrediente_widget)

    def insert_screen_step3(self):
        insert_step3_widget = QWidget()
        layout = QVBoxLayout()

        # Configuração da imagem ilustrativa
        cooking_image_path = 'modo_preparo.jpg'  # Atualize com o caminho correto
        cooking_image_label = QLabel()
        cooking_image_pixmap = QPixmap(cooking_image_path)
        cooking_image_label.setPixmap(cooking_image_pixmap.scaled(600, 400, Qt.KeepAspectRatio))
        cooking_image_label.setAlignment(Qt.AlignCenter)

        # Configuração da caixa de texto grande para o modo de preparo
        self.modo_preparo_edit = QTextEdit()
        self.modo_preparo_edit.setPlaceholderText("Digite o modo de preparo aqui...")
        self.modo_preparo_edit.setFont(QFont("Arial", 12))
        self.modo_preparo_edit.setMinimumHeight(200)  # Altura mínima para a caixa de texto

        # Botões de seleção de imagem e bandeira
        select_image_button = QPushButton("Selecionar Imagem da Receita")
        select_image_button.clicked.connect(self.select_image)

        select_bandeira_button = QPushButton("Selecionar Imagem da Bandeira")
        select_bandeira_button.clicked.connect(self.select_bandeira)

        submit_button = QPushButton("Salvar Receita")
        submit_button.clicked.connect(self.save_recipe)

        # Adicionando todos os componentes ao layout
        layout.addWidget(cooking_image_label)
        layout.addWidget(QLabel("Modo de Preparo:"))
        layout.addWidget(self.modo_preparo_edit)
        layout.addWidget(select_image_button)
        layout.addWidget(select_bandeira_button)
        layout.addWidget(submit_button)

        # Ajustando o layout para expandir a caixa de texto horizontalmente
        layout.setStretchFactor(self.modo_preparo_edit, 1)

        insert_step3_widget.setLayout(layout)
        self.stacked_widget.addWidget(insert_step3_widget)
        self.add_back_button(layout, 2)

    def select_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem da Receita", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_name:
            self.imagem_path = file_name

    def select_bandeira(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem da Bandeira", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_name:
            self.bandeira_path = file_name

    def save_recipe(self):
        nome_popular = self.nome_popular_edit.text()
        tipo = self.tipo_combo.currentText()
        categoria = self.categoria_combo.currentText()
        tipo_prato = self.tipo_prato_combo.currentText()
        origem = self.origem_combo.currentText()
        tempo_preparo = self.tempo_preparo_spin.value()
        modo_preparo = self.modo_preparo_edit.text()

        ingredientes = []
        for i in range(self.ingredientes_layout.count()):
            widget = self.ingredientes_layout.itemAt(i).widget()
            if widget:
                nome = widget.layout().itemAt(0).widget().text()
                quantidade = widget.layout().itemAt(1).widget().value()
                unidade = widget.layout().itemAt(2).widget().currentText()
                ingredientes.append({"nome": nome, "quantidade": quantidade, "unidade": unidade})

        imagem_id = None
        if self.imagem_path:
            with open(self.imagem_path, "rb") as image_file:
                imagem_id = fs.put(image_file, filename=self.imagem_path.split('/')[-1])

        bandeira_id = None
        if self.bandeira_path:
            with open(self.bandeira_path, "rb") as bandeira_file:
                bandeira_id = fs.put(bandeira_file, filename=self.bandeira_path.split('/')[-1])

        receita = Receita(
            nome_popular=nome_popular,
            tipo=tipo,
            categoria=categoria,
            tipo_prato=tipo_prato,
            origem=origem,
            tempo_preparo=tempo_preparo,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            imagem_id=imagem_id,
            bandeira_origem_id=bandeira_id
        )

        db.receitas.insert_one(receita.to_dict())
        self.stacked_widget.setCurrentIndex(0)  # Voltar para a tela inicial após salvar

    def query_screen(self):
        query_widget = QWidget()
        layout = QVBoxLayout()

        self.query_tipo_combo = QComboBox()
        self.query_tipo_combo.addItems(["", "Líquido", "Sólido"])
        self.query_categoria_combo = QComboBox()
        self.query_categoria_combo.addItems(["", "Café da manhã", "Almoço", "Jantar"])
        self.query_tipo_prato_combo = QComboBox()
        self.query_tipo_prato_combo.addItems(["", "Prato principal", "Aperitivo", "Sobremesa"])
        self.query_origem_combo = QComboBox()
        self.populate_country_combobox(self.query_origem_combo, include_empty=True)

        self.query_result_list = QListWidget()
        self.query_result_list.itemClicked.connect(self.display_recipe_details)

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.perform_query)

        layout.addWidget(QLabel("Tipo:"))
        layout.addWidget(self.query_tipo_combo)
        layout.addWidget(QLabel("Categoria:"))
        layout.addWidget(self.query_categoria_combo)
        layout.addWidget(QLabel("Tipo de Prato:"))
        layout.addWidget(self.query_tipo_prato_combo)
        layout.addWidget(QLabel("País de Origem:"))
        layout.addWidget(self.query_origem_combo)
        layout.addWidget(search_button)
        layout.addWidget(QLabel("Resultados:"))
        layout.addWidget(self.query_result_list)

        query_widget.setLayout(layout)
        self.stacked_widget.addWidget(query_widget)
        self.query_result_list.itemClicked.connect(self.display_recipe_details)
        self.add_back_button(layout)

    def populate_country_combobox(self, combobox, include_empty=False):
        countries = [
            "Brasil", "Estados Unidos", "França", "Alemanha", "Itália", "Japão", "México", "Espanha", "Reino Unido"
        ]
        if include_empty:
            combobox.addItem("")
        for country in countries:
            combobox.addItem(country)

    def perform_query(self):
        tipo = self.query_tipo_combo.currentText()
        categoria = self.query_categoria_combo.currentText()
        tipo_prato = self.query_tipo_prato_combo.currentText()
        origem = self.query_origem_combo.currentText()

        query = {}
        if tipo:
            query["tipo"] = tipo
        if categoria:
            query["categoria"] = categoria
        if tipo_prato:
            query["tipo_prato"] = tipo_prato
        if origem:
            query["origem"] = origem

        results = db.receitas.find(query)
        self.query_result_list.clear()
        for result in results:
            item = QListWidgetItem(result["nome_popular"])
            self.query_result_list.addItem(item)
            

    def display_recipe_details(self, item):
        recipe_name = item.text()
        recipe = db.receitas.find_one({"nome_popular": recipe_name})

        if recipe:
            details_widget = QWidget()
            main_layout = QVBoxLayout(details_widget)
            top_layout = QHBoxLayout()
            bottom_layout = QGridLayout()

            # Image
            image_label = QLabel()
            if recipe.get("imagem_id"):
                pixmap = QPixmap()
                pixmap.loadFromData(fs.get(recipe["imagem_id"]).read())
                image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
            else:
                image_label.setText("Imagem não Disponível")
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("background-color: gray; font-size: 16px;")
                image_label.setFixedSize(400, 400)

            # Title
            title_label = QLabel(recipe["nome_popular"])
            title_label.setFont(QFont("Georgia", 24, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)

            # Flag
            flag_label = QLabel()
            if recipe.get("bandeira_origem_id"):
                flag_pixmap = QPixmap()
                flag_pixmap.loadFromData(fs.get(recipe["bandeira_origem_id"]).read())
                flag_label.setPixmap(flag_pixmap.scaled(50, 50, Qt.KeepAspectRatio))
            else:
                flag_label.setText("Bandeira não disponível")
                flag_label.setAlignment(Qt.AlignRight)
                flag_label.setStyleSheet("font-size: 12px;")

            top_layout.addWidget(image_label)
            top_layout.addSpacing(20)
            top_layout.addWidget(title_label)
            top_layout.addWidget(flag_label)
            top_layout.setAlignment(flag_label, Qt.AlignTop | Qt.AlignRight)

            # Ingredients and Preparation
            ingredients_label = QLabel("Ingredientes:")
            ingredients_label.setFont(QFont("Arial", 18))
            ingredients_text = QLabel("\n".join([f"{ing['quantidade']} {ing['unidade']} de {ing['nome']}" for ing in recipe["ingredientes"]]))
            ingredients_text.setFont(QFont("Arial", 14))
            ingredients_text.setWordWrap(True)

            preparation_label = QLabel("Modo de Preparo:")
            preparation_label.setFont(QFont("Arial", 18))
            preparation_text = QLabel(recipe["modo_preparo"])
            preparation_text.setFont(QFont("Arial", 14))
            preparation_text.setWordWrap(True)

            # Grid layout for text alignment
            bottom_layout.addWidget(ingredients_label, 0, 0)
            bottom_layout.addWidget(ingredients_text, 1, 0)
            bottom_layout.addWidget(preparation_label, 0, 1)
            bottom_layout.addWidget(preparation_text, 1, 1)
            bottom_layout.setColumnStretch(1, 2)

            main_layout.addLayout(top_layout)
            main_layout.addLayout(bottom_layout)

            self.stacked_widget.addWidget(details_widget)
            self.stacked_widget.setCurrentWidget(details_widget)
            self.add_back_button(main_layout, 4)
