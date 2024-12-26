import os
import subprocess
import sys
import time
import ruamel.yaml
from PyQt5.QtCore import QProcess, QUrl, Qt
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5 import QtWidgets, QtCore, QtGui
from configuration import tishi
from configuration import edit
from configuration.home import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication


class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.process = None
        self.init_ui()

    def init_ui(self):
        self.initial()
        self.toolButton.clicked.connect(self.sqlmap_file) 
        self.pushButton_3.clicked.connect(self.sqlmap_start)
        self.pushButton_4.clicked.connect(self.cmd_start)
        self.toolButton_2.clicked.connect(self.r_file)
        self.toolButton_3.clicked.connect(self.m_file)
        self.pushButton_9.clicked.connect(self.open_folder)
        self.pushButton_7.clicked.connect(self.sqlmap_help)
        self.pushButton_6.clicked.connect(self.clear_cmd)
        self.pushButton_5.clicked.connect(self.sqlmap_update)
        self.pushButton_10.clicked.connect(self.Command_line) 
        self.pushButton.clicked.connect(self.sqlmap_zr) 

       
       
        self.textEdit.setFocus()
        self.textEdit.installEventFilter(self) 

    def initial(self):
        if os.path.exists('file_address.yaml'):
            with open('file_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.lineEdit.setText(config['sqlmap_address'])
                self.lineEdit_12.setText(config['address'] + '/log/')

    def sqlmap_start(self):
        self.process_kill()
        self.process_creation()
        self.process.start(self.Command_line())

    def cmd_start(self):
        cmd_line = self.Command_line()
        if cmd_line != None:
            command = f'cmd.exe /k {cmd_line}'
            process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def Command_line(self):
        args = "python " + self.lineEdit.text()
        if self.radioButton.isChecked():
            if self.lineEdit_3.text() != "":
                args += " -u \"" + self.lineEdit_3.text() + "\""
            else:
                text = '未设置URL'
                img = './img/失败.PNG'
                self.open_tishiwindow(text, img)
                return
        if self.radioButton_3.isChecked():
            if self.lineEdit_4.text() != "":
                if os.path.exists(self.lineEdit_4.text()):
                    args += " -r " + self.lineEdit_4.text()
                else:
                    text = '未找到request文件'
                    img = './img/失败.PNG'
                    self.open_tishiwindow(text, img)
                    return
            else:
                text = '未设置request文件'
                img = './img/失败.PNG'
                self.open_tishiwindow(text, img)
                return
        if self.radioButton_4.isChecked():
            if self.lineEdit_5.text() != "":
                if os.path.exists(self.lineEdit_5.text()):
                    args += " -m " + self.lineEdit_5.text()
                else:
                    text = '未找到url列表文件'
                    img = './img/失败.PNG'
                    self.open_tishiwindow(text, img)
                    return
            else:
                text = '未设置url列表文件'
                img = './img/失败.PNG'
                self.open_tishiwindow(text, img)
                return

       
        tamper_map = {
            self.checkBox: "B",
            self.checkBox_2: "Q",
            self.checkBox_3: "T",
            self.checkBox_4: "U",
            self.checkBox_5: "E",
            self.checkBox_6: "S"
        }

       
        if any(cb.isChecked() for cb in tamper_map):
            args += " --technique "

       
        for checkbox, char in tamper_map.items():
            if checkbox.isChecked():
                args += char

        current_map = {
            self.checkBox_7: " --current-db",
            self.checkBox_8: " --dbs",
            self.checkBox_9: " --tables",
            self.checkBox_10: " --columns",
            self.checkBox_11: " --dump-all",
            self.checkBox_12: " --identify-waf",
            self.checkBox_13: " -a",
            self.checkBox_14: " -b",
            self.checkBox_15: " --batch",
            self.checkBox_16: " --flush-session",
            self.checkBox_17: " --force-ssl",
            self.checkBox_18: " -o",
            self.checkBox_19: " --os-shell",
        }
        for checkbox, char in current_map.items():
            if checkbox.isChecked():
                args += char

        appoint_map = {
            self.lineEdit_7: " -D " + self.lineEdit_7.text(),
            self.lineEdit_8: " -T " + self.lineEdit_8.text(),
            self.lineEdit_9: " -C " + self.lineEdit_9.text(),
            self.lineEdit_11: " -p " + self.lineEdit_11.text(),
            self.lineEdit_2: " --thread " + self.lineEdit_2.text(),
            self.lineEdit_6: " -timeout " + self.lineEdit_6.text(),
        }

        add_dump = False
        for checkbox, char in appoint_map.items():
            if checkbox.text() != "":
                args += char
                # 检查是否有 -D, -T, -C 参数
                if "-D" in char or "-T" in char or "-C" in char:
                    add_dump = True
        if add_dump:
            args += " --dump"

        QComboBox_map = {
            self.comboBox_3: " --dbms=" + self.comboBox_3.currentText(),
            self.comboBox: " --level " + self.comboBox.currentText(),
            self.comboBox_2: " --risk " + self.comboBox_2.currentText(),
            self.comboBox_4: " -v " + self.comboBox_4.currentText(),
        }

        for checkbox, char in QComboBox_map.items():
            if checkbox.currentText() != "":
                args += char

        if self.checkBox_21.isChecked():
            args += " --cookie=\"" + self.lineEdit_13.text() + "\""

        if self.checkBox_20.isChecked():
            args += " --proxy=" + self.lineEdit_10.text()

        if self.radioButton_2.isChecked():
            args += " --output-dir=" + self.lineEdit_12.text()

        self.textEdit.append(f'<span style="color:orange;">{args}</span>')

        return args

   
    def sqlmap_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*.py);")
        if fileName:
            self.lineEdit.setText(fileName)
            self.lineEdit_12.setText(os.getcwd().replace('\\', '/') + '/log/')
            self.process_kill()
            if os.path.exists('file_address.yaml'):
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    config['sqlmap_address'] = fileName
                    config['address'] = os.getcwd().replace('\\', '/')
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml.dump(config, file)
                self.process_creation()
                self.process.start("python " + fileName)
            else:
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    yaml.dump({'sqlmap_address': fileName}, file)
                    yaml.dump({'address': os.getcwd().replace('\\', '/')}, file)
                self.process_creation()
                self.process.start("python " + fileName)

    def r_file(self):
        if self.lineEdit.text() == "":
            text = '未设置sqlmap文件'
            img = './img/失败.PNG'
            self.open_tishiwindow(text, img)
            return
        self.radioButton_3.setChecked(True)
        with open('file_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            request_file_path = config['address'] + '/request_list/' + str(int(time.time())) + '.txt'
            self.lineEdit_4.setText(request_file_path)
            self.edit_txt(request_file_path, "request文件")

    def m_file(self):
        if self.lineEdit.text() == "":
            text = '未设置sqlmap文件'
            img = './img/失败.PNG'
            self.open_tishiwindow(text, img)
            return
        self.radioButton_4.setChecked(True)
        with open('file_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            request_file_path = config['address'] + '/url_list/' + str(int(time.time())) + '.txt'
            self.lineEdit_5.setText(request_file_path)
            self.edit_txt(request_file_path, "URL列表文件")

    def open_folder(self):
       
        url = QUrl.fromLocalFile(self.lineEdit_12.text())
        QDesktopServices.openUrl(url)

   
    def clear_cmd(self):
        self.textEdit.clear()
        self.process_kill()

    def sqlmap_update(self):
        command = f'cmd.exe /k python {self.lineEdit.text()} --update"'
        process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def sqlmap_help(self):
        self.process_kill()
        self.process_creation()
        self.process.start("python " + self.lineEdit.text() + " -h")

    def sqlmap_zr(self):
       
        checkboxes = [
            self.checkBox,
            self.checkBox_2,
            self.checkBox_3,
            self.checkBox_4,
            self.checkBox_5,
            self.checkBox_6
        ]

       
        all_checked = all(checkbox.isChecked() for checkbox in checkboxes)

       
        for checkbox in checkboxes:
            checkbox.setChecked(not all_checked)

   
    def process_creation(self):
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.handle_finished)

   
    def handle_output(self):
        try:
            data = self.process.readAll().data().decode('utf-8').strip()
            lines = data.split('\n')
            for line in lines:
                self.append_colored_output(line)
        except:
            data = self.process.readAll().data().decode('latin-1').strip()
            lines = data.split('\n')
            for line in lines:
                self.append_colored_output(line)

   
    def append_colored_output(self, line):
       
        if "[INFO]" in line: 
            self.textEdit.append(f'<span style="color:green;">{line}</span>')
        elif "Type:" in line or "Title:" in line or "Payload:" in line: 
            self.textEdit.append(f'<span style="color:red;">{line}</span>')
        elif "[WARNING]" in line: 
            self.textEdit.append(f'<span style="color:orange;">{line}</span>')
        elif "[ERROR]" in line: 
            self.textEdit.append(f'<span style="color:red;">{line}</span>')
        elif "[CRITICAL]" in line: 
            self.textEdit.append(f'<span style="color:blue;">{line}</span>')
        else: 
            self.textEdit.append(f'<span style="color:white;">{line}</span>')

   
    def handle_finished(self):
        self.process.deleteLater()
        self.process = None

   
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.textEdit:
            if event.key() == QtCore.Qt.Key_Return:
               
                cursor = self.textEdit.textCursor()

               
                user_input = cursor.block().text().strip()

                if user_input: 

                   
                    self.textEdit.append('')

                   
                    if self.process is not None and self.process.state() == QProcess.Running:
                        self.process.write((user_input + "\n").encode('utf-8'))

               
                new_cursor = self.textEdit.textCursor()
                new_cursor.movePosition(QtGui.QTextCursor.End)
                self.textEdit.setTextCursor(new_cursor)

                return True 
        return super().eventFilter(source, event)

   
    def process_kill(self):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished() 

    def edit_txt(self, text, window_title):
        self.edit_window = edit.Edit()
        self.edit_window.edit_file = text
        icon = QIcon('img/logo.png')
        self.edit_window.setWindowIcon(icon)
        self.edit_window.setWindowTitle(window_title) 
        self.edit_window.setWindowModality(Qt.ApplicationModal)
       
        main_geometry = self.geometry()
        main_x = main_geometry.x()
        main_y = main_geometry.y()
        main_width = main_geometry.width()
        main_height = main_geometry.height()
        self.edit_window.move(main_x + (main_width - self.edit_window.width()) // 2,
                              main_y + (main_height - self.edit_window.height()) // 2)
        self.edit_window.show()

   
    def open_tishiwindow(self, text, img):
        self.tishi_window = tishi.TiShi()
        icon = QIcon('img/logo.png')
        self.tishi_window.setWindowIcon(icon)
        if text:
            self.tishi_window.label.setText(text)
        if img:
            self.tishi_window.label_2.setPixmap(QtGui.QPixmap(img))
        self.tishi_window.setWindowModality(Qt.ApplicationModal) 
       
        main_geometry = self.geometry()
        main_x = main_geometry.x()
        main_y = main_geometry.y()
        main_width = main_geometry.width()
        main_height = main_geometry.height()

       
        tishi_width = self.tishi_window.width()
        tishi_height = self.tishi_window.height()

       
        tishi_x = main_x + (main_width - tishi_width) // 2
        tishi_y = main_y + (main_height - tishi_height) // 2

       
        self.tishi_window.move(tishi_x, tishi_y)
        self.tishi_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    icon = QIcon('./img/logo.png')
    w.setWindowIcon(icon)
    w.show()
    sys.exit(app.exec_())
