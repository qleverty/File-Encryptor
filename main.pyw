import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QRadioButton, 
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont
from cryptography.fernet import Fernet, InvalidToken

key = b"AA8jMXhUiJZyp56OZdz3lQpXwaSSekrTi1znzCvW4I8="

def encrypt_file(file_path):
    with open(file_path, "rb") as file:
        original_data = file.read()
    encrypted_data = Fernet(key).encrypt(original_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = Fernet(key).decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("File is not encrypted or has been tampered with.")
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

class FileEncryptorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_exists = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Encryptor")
        self.setFixedSize(300, 80)
        self.setStyleSheet("background-color: #373d3b;")
        
        font = QFont("Xolonium", 10)
        self.setFont(font)

        main_layout = QVBoxLayout()
        file_layout = QHBoxLayout()
        action_layout = QHBoxLayout()

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("Enter file directory...")
        self.file_input.setStyleSheet("background-color: #3b3b3b; color: #e8e8e8; border: 1px solid #2c2c2c; padding: 5px;")
        self.file_input.textChanged.connect(self.check_file)
        
        self.browse_button = QPushButton("...", self)
        self.browse_button.setStyleSheet("background-color: #df7126; color: white; border: 1px solid #a7551d; padding: 5px;")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        self.encrypt_radio = QRadioButton("Encrypt", self)
        self.encrypt_radio.setStyleSheet("color: #e8e8e8;")
        self.decrypt_radio = QRadioButton("Decrypt", self)
        self.decrypt_radio.setStyleSheet("color: #e8e8e8;")
        
        self.encrypt_radio.toggled.connect(self.update_accept_button_state)
        self.decrypt_radio.toggled.connect(self.update_accept_button_state)

        self.accept_button = QPushButton("Accept", self)
        self.accept_button.setStyleSheet("background-color: #316f31; color: white; border: 1px solid #245424; padding: 5px;")
        self.accept_button.clicked.connect(self.perform_action)
        self.accept_button.setEnabled(False)

        action_layout.addWidget(self.encrypt_radio)
        action_layout.addWidget(self.decrypt_radio)
        action_layout.addWidget(self.accept_button)

        main_layout.addLayout(file_layout)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            self.file_input.setText(file_path)

    def update_accept_button_state(self):
        s = self.file_exists and (self.encrypt_radio.isChecked() or self.decrypt_radio.isChecked())
        self.accept_button.setStyleSheet("background-color: #4cae4c; color: white; border: 1px solid #398339; padding: 5px;"
                                         if s else "background-color: #316f31; color: white; border: 1px solid #245424; padding: 5px;")
        self.accept_button.setEnabled(s)
        
    def check_file(self):
        s = os.path.isfile(self.file_input.text())
        self.file_input.setStyleSheet("background-color: #3b3b3b; color: #e8e8e8; border: 1px solid #2c2c2c; padding: 5px;"
                                      if s else "background-color: #392828; color: #e8e8e8; border: 1px solid #9d3131; padding: 5px;")
        self.file_exists = s
        self.update_accept_button_state()

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setStyleSheet("background-color: #373d3b; color: white;")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setStyleSheet("background-color: #444444; color: white; border: none; padding: 7px;")
        msg_box.exec_()

    def perform_action(self):
        file_path = self.file_input.text()
        if self.encrypt_radio.isChecked():
            try:
                encrypt_file(file_path)
                self.show_message("Success", "File encrypted successfully!")
            except Exception as e:
                self.show_message("Error", str(e))
        elif self.decrypt_radio.isChecked():
            try:
                decrypt_file(file_path)
                self.show_message("Success", "File decrypted successfully!")
            except Exception as e:
                self.show_message("Error", str(e))

app = QApplication(sys.argv)
window = FileEncryptorApp()
window.show()
sys.exit(app.exec_())
