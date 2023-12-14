









from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(907, 717)
        self.gridLayout_7 = QtWidgets.QGridLayout(Form)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit_5 = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEdit_5.setObjectName("textEdit_5")
        self.gridLayout_5.addWidget(self.textEdit_5, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_5, 5, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_2.addWidget(self.textEdit_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_3 = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout_3.addWidget(self.textEdit_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(Form)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_7.addWidget(self.groupBox_7, 0, 1, 7, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit_4 = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_4.setObjectName("textEdit_4")
        self.gridLayout_4.addWidget(self.textEdit_4, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_4, 3, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(Form)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.textEdit_6 = QtWidgets.QTextEdit(self.groupBox_6)
        self.textEdit_6.setObjectName("textEdit_6")
        self.gridLayout_6.addWidget(self.textEdit_6, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_6, 6, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_5.setTitle(_translate("Form", "Unicode与中文互转"))
        self.groupBox_2.setTitle(_translate("Form", "Url"))
        self.groupBox_3.setTitle(_translate("Form", "Base64"))
        self.pushButton_2.setText(_translate("Form", "加密"))
        self.pushButton.setText(_translate("Form", "解密"))
        self.groupBox.setTitle(_translate("Form", "Text"))
        self.groupBox_4.setTitle(_translate("Form", "Hex"))
        self.groupBox_6.setTitle(_translate("Form", "MD5"))
