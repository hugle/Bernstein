from PyQt5.QtWidgets import *


class Form(QWidget):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        main_layout = QGridLayout()
        name_label = QLabel("Attribute Name :")
        self.nameLine = QLineEdit()
        self.submitButton = QPushButton("Add")

        button_layout = QVBoxLayout()
        button_layout.addWidget(name_label)
        button_layout.addWidget(self.nameLine)
        button_layout.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submit_contact)

        main_layout.addLayout(button_layout, 0, 1)

        self.setLayout(main_layout)
        self.setWindowTitle("Hello Qt")

    def submit_contact(self):
        name = self.nameLine.text()

        if name == "":
            QMessageBox.information(self, "Empty Field",
                                    "Please enter a name and address.")
        else:
            QMessageBox.information(self, "Success!",
                                    "Hello %s!" % name)
