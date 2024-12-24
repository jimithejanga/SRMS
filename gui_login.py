from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
import sys
from gui_main import SchoolManagementSystem  # Import your main GUI class


class LoginPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # Username and Password Fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Placeholder logic for authentication
        if username == "admin" and password == "password":  # Replace with real logic
            self.accept()  # Close the dialog and return success
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show login page
    login = LoginPage()
    if login.exec() == QDialog.Accepted:
        # Open main application after successful login
        main_window = SchoolManagementSystem()
        main_window.show()
        sys.exit(app.exec())
