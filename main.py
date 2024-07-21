import sys
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow

def apply_dark_theme(app):
    app.setStyleSheet("""
    QWidget {
        color: #b1b1b1;
        background-color: #323232;
    }
    QLabel {
        color: #ffffff;
    }
    QPushButton {
        background-color: #5c5c5c;
        border: 2px solid #5c5c5c;
        border-radius: 10px;
        padding: 10px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #505050;
        border: 2px solid #505050;
    }
    QLineEdit {
        background-color: #424242;
        border: 2px solid #424242;
        border-radius: 5px;
        padding: 5px;
        color: #ffffff;
    }
    QListWidget {
        background-color: #424242;
        color: #ffffff;
    }
    QComboBox {
        background-color: #424242;
        color: #ffffff;
        border-radius: 5px;
        padding: 5px;
    }
    QSpinBox {
        background-color: #424242;
        color: #ffffff;
        border: none;
    }
    """)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)  # Aplica o tema escuro antes de criar a janela principal
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
