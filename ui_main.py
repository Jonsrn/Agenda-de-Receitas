from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QPushButton, QLabel, 
    QComboBox, QLineEdit, QDialog, QFileDialog, QListWidget, QListWidgetItem, 
    QFormLayout, QSpinBox, QHBoxLayout, QGridLayout, QFrame
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

    def home_screen(self):
        home_widget = QWidget()
        layout = QVBoxLayout()

        insert_button = QPushButton("Inserir Receita")
        insert_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        query_button = QPushButton("Consultar Receita")
        query_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        layout.addWidget(insert_button)
        layout.addWidget(query_button)
        home_widget.setLayout(layout)

        self.stacked_widget.addWidget(home_widget)

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

        self.modo_preparo_edit = QLineEdit()
        self.imagem_path = ""
        self.bandeira_path = ""

        select_image_button = QPushButton("Selecionar Imagem da Receita")
        select_image_button.clicked.connect(self.select_image)

        select_bandeira_button = QPushButton("Selecionar Imagem da Bandeira")
        select_bandeira_button.clicked.connect(self.select_bandeira)

        layout.addWidget(QLabel("Modo de Preparo:"))
        layout.addWidget(self.modo_preparo_edit)
        layout.addWidget(select_image_button)
        layout.addWidget(select_bandeira_button)

        submit_button = QPushButton("Salvar Receita")
        submit_button.clicked.connect(self.save_recipe)
        layout.addWidget(submit_button)
        insert_step3_widget.setLayout(layout)

        self.stacked_widget.addWidget(insert_step3_widget)

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
