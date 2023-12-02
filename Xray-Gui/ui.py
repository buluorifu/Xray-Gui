import sys
from PyQt5.QtGui import QIcon
from configuration.box1 import BOX1
from configuration.box2 import BOX2
from configuration.homepage import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout


class MyWindow(QWidget,Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)  
        self.init_ui()
        self.sub_window = None  

    def init_ui(self):
        self.qsl = QStackedLayout(self.groupBox_2)
        self.box1 = BOX1()
        self.box2 = BOX2()
        
        self.qsl.addWidget(self.box1)
        self.qsl.addWidget(self.box2)

        
        self.pushButton.clicked.connect(self.btn_press1_clicked)
        self.pushButton_2.clicked.connect(self.btn_press2_clicked)
        self.pushButton_3.clicked.connect(self.btn_press3_clicked)

    def btn_press1_clicked(self):
        
        self.qsl.setCurrentIndex(0)

    def btn_press2_clicked(self):
        
        self.qsl.setCurrentIndex(2)

    def btn_press3_clicked(self):
        
        self.qsl.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    icon = QIcon('./img/扫描.png')
    w.setWindowIcon(icon)
    w.show()
    sys.exit(app.exec_())