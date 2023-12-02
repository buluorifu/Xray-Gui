from PyQt5.QtCore import Qt, pyqtSignal
from .tishi_ui import Ui_Form
from PyQt5.QtWidgets import QWidget


class TiShi(QWidget,Ui_Form):
    closed = pyqtSignal()  
    def __init__(self):
        super(TiShi, self).__init__()
        self.setupUi(self)  

        self.setWindowFlags(Qt.WindowCloseButtonHint)  

        def closeEvent(self, event):
            self.closed.emit()  
            event.accept()