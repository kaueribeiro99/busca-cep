import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import requests

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Buscador de CEP'
        self.left = 100
        self.top = 200
        self.width = 250
        self.height = 120
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #cria a label
        self.label = QLabel(self)
        self.label.setText('Digite o CEP:')
        self.label.resize(200, 40)
        self.label.move(20, 0)
        self.label.setStyleSheet('QLabel {font:bold; font-size:14px}')

        # Cria o textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 35)
        self.textbox.resize(200,20)
        
        # Cria um botão na janela
        self.button = QPushButton('Buscar', self)
        self.button.move(127,80)
        
        # Conecta o botão no método on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()
    def on_click(self):
        cep = self.buscacep()
        if cep == 'CEP inválido':
            QMessageBox.question(self, 'Procura CEP', "Você digitou um CEP inválido ", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Procura CEP', "Local Encontrado: " + cep, QMessageBox.Ok, QMessageBox.Ok)

        self.textbox.setText("")


    def buscacep(self):
        cep = self.textbox.text()
        request = requests.get(f'http://viacep.com.br/ws/{cep}/json/')
        dir(request)

        try:
            dicionario = request.json()
            uf = dicionario['uf']
            rua = dicionario['logradouro']
            bairro = dicionario['bairro']
            cidade = dicionario['localidade']
            print(f' {rua}, {bairro} - {cidade} {uf}')
            return f' {rua}, {bairro} - {cidade} {uf}'
        except:
            return 'CEP inválido'
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())