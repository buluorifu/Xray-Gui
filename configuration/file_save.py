from .file_save_ui import Ui_Form
from PyQt5.QtWidgets import QWidget

class file_win(QWidget,Ui_Form):
    def __init__(self):
        super(file_win, self).__init__()
        self.setupUi(self)  

