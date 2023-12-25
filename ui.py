import sys
from PyQt5.QtGui import QIcon
from configuration.box1 import BOX1
from configuration.box2 import BOX2
from configuration.box3 import BOX3
from configuration.homepage import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout


class MyWindow(QWidget,Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)  # 使用 sjui.Ui_Form 类中的方法初始化 UI
        self.init_ui()
        self.sub_window = None  # 存储子窗口对象的属性

    def init_ui(self):
        self.qsl = QStackedLayout(self.groupBox_2)
        self.box1 = BOX1()
        self.box2 = BOX2()
        self.box3 = BOX3()

        self.qsl.addWidget(self.box1)
        self.qsl.addWidget(self.box2)
        self.qsl.addWidget(self.box3)

        # 给按钮添加事件（即点击后要调用的函数）
        self.pushButton.clicked.connect(self.btn_press1_clicked)
        self.pushButton_2.clicked.connect(self.btn_press2_clicked)
        self.pushButton_3.clicked.connect(self.btn_press3_clicked)
# 设置按钮1的初始样式
        self.pushButton.setStyleSheet("background-color: #CAE1FF;")

    def btn_press1_clicked(self):
        self.qsl.setCurrentIndex(0)
        self.pushButton.setStyleSheet("background-color: #CAE1FF;")
        self.pushButton_2.setStyleSheet("")  # 恢复按钮2的默认样式
        self.pushButton_3.setStyleSheet("")  # 恢复按钮3的默认样式

    def btn_press2_clicked(self):
        self.qsl.setCurrentIndex(1)
        self.pushButton.setStyleSheet("")  # 恢复按钮1的默认样式
        self.pushButton_2.setStyleSheet("background-color: #CAE1FF;")
        self.pushButton_3.setStyleSheet("")  # 恢复按钮3的默认样式

    def btn_press3_clicked(self):
        self.qsl.setCurrentIndex(2)
        self.pushButton.setStyleSheet("")  # 恢复按钮1的默认样式
        self.pushButton_2.setStyleSheet("")  # 恢复按钮2的默认样式
        self.pushButton_3.setStyleSheet("background-color: #CAE1FF;")

    def closeEvent(self, event):
        # 关闭其他窗口的代码
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QWidget) and widget != self:
                widget.close()

        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    icon = QIcon('./img/扫描.png')
    w.setWindowIcon(icon)
    w.show()
    sys.exit(app.exec_())
