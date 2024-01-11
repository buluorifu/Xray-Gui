import os
import re
import time
from PyQt5.QtGui import QIcon
from . import config
import ruamel.yaml
from PyQt5.QtCore import QProcess, Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from . import tishi
from .box1_ui import Ui_Form

class BOX1(QWidget,Ui_Form):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)  # 使用 sjui.Ui_Form 类中的方法初始化 UI
        self.init_ui()
        self.config_window = None
        self.process = None
        self.args = None
        self.dict = {'name':str(int(time.time())),'name_all':'','url':'','request':'','url_list':''}

    def init_ui(self):
        self.initial()
        self.pushButton_8.clicked.connect(self.open_subwindow)
        self.toolButton.clicked.connect(self.xray_file)         # 读取xray文件
        self.pushButton.clicked.connect(self.basics_save)       # 确认修改基础配置
        self.pushButton_6.clicked.connect(self.clear_cmd)       # 清空命令行输出
        self.pushButton_5.clicked.connect(self.xray_version)    # 查看xray版本
        self.pushButton_2.clicked.connect(self.name_save)       # 生成word名字
        self.lineEdit_3.textChanged.connect(self.url_save)      # 输入url保存
        self.toolButton_2.clicked.connect(self.request_body)    # 选取request文件保存
        self.toolButton_3.clicked.connect(self.url_list_save)   # 选取url_list文件保存
        self.pushButton_3.clicked.connect(self.initiative_scan) # 开启主动扫描
        self.pushButton_4.clicked.connect(self.passive_scan)    # 开启被动扫描
        self.pushButton_9.clicked.connect(self.file_look)       # 查看扫描结果
        self.pushButton_10.clicked.connect(self.command_look)   # 查看当前命令
        self.pushButton_7.clicked.connect(self.poc_start)       # 访问编写poc网址

    # 加载上一次选项
    def initial(self):
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.spinBox.setValue(int(config['parallel']))
                self.spinBox_2.setValue(int(config['http']['dial_timeout']))
                self.spinBox_3.setValue(int(config['http']['max_redirect']))
                self.spinBox_4.setValue(int(config['http']['max_qps']))
        if os.path.exists('file_address.yaml'):
            with open('file_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.lineEdit.setText(config['xray_address'])

    # 确认修改基础配置
    def basics_save(self):
        if os.path.exists('file_address.yaml'):
            with open('config.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                config['parallel'] = int(self.spinBox.text())
                config['http']['dial_timeout'] = int(self.spinBox_2.text())
                config['http']['max_redirect'] = int(self.spinBox_3.text())
                config['http']['max_qps'] = int(self.spinBox_4.text())
            with open('config.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(config, file)
            self.open_tishiwindow(None, None)
        else:
            text = '未配置xray文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)


    # 生成word名字
    def name_save(self):
        if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
            self.dict['name'] = str(int(time.time()))
        else:
            self.dict['name'] = self.lineEdit_2.text()
        self.open_tishiwindow(None, None)

    # 访问编写poc网址
    def poc_start(self):
        url = QtCore.QUrl('https://poc.xray.cool/')
        QtGui.QDesktopServices.openUrl(url)

    # 输入url保存
    def url_save(self):
        self.dict['url']=self.lineEdit_3.text()
        self.dict['request']=''
        self.dict['url_list']=''
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

    # 选取request文件保存
    def request_body(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);")
        self.dict['url'] = ''
        self.dict['request'] = fileName
        self.dict['url_list'] = ''
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText(fileName)
        self.lineEdit_5.setText('')

    # 选取url_list文件保存
    def url_list_save(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);")
        self.dict['url'] = ''
        self.dict['request'] = ''
        self.dict['url_list'] = fileName
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText(fileName)

    # 查看扫描结果
    def file_look(self):
        try:
            if self.dict['name_all']:
                os.startfile(self.dict['name_all'])
            else:
                text = '没有输出文件'
                img = './img/失败.png'
                self.open_tishiwindow(text, img)
        except:
                text = '没有输出文件'
                img = './img/失败.png'
                self.open_tishiwindow(text, img)

    # 开启主动扫描
    def initiative_scan(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            if not hasattr(self, 'is_first_click'):
                if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
                    self.dict['name'] = str(int(time.time()))
                else:
                    self.dict['name'] = self.lineEdit_2.text()
                # 第一次按下按钮
                self.is_first_click = True
                self.process_kill()
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    self.args = config['xray_address']
                    if self.radioButton_5.isChecked():
                        self.args = self.args + ' --log-level debug'
                    if self.radioButton_6.isChecked():
                        self.args = self.args + ' --log-level info'
                    if self.radioButton_7.isChecked():
                        self.args = self.args + ' --log-level warn'
                    if self.radioButton_8.isChecked():
                        self.args = self.args + ' --log-level error'
                    if self.radioButton_9.isChecked():
                        self.args = self.args + ' --log-level fatal'
                    self.args = self.args + ' webscan'
                    if self.radioButton_11.isChecked():
                        self.args = self.args + ' --level medium'
                    if self.radioButton_12.isChecked():
                        self.args = self.args + ' --level high'
                    if self.radioButton_13.isChecked():
                        self.args = self.args + ' --level critical'
                    if self.dict['url']:
                        self.args = self.args + ' --url ' + self.dict['url']
                    if self.dict['request']:
                        self.args = self.args + ' --raw-request ' + self.dict['request']
                    if self.dict['url_list']:
                        self.args = self.args + ' --url-file ' + self.dict['url_list']
                    if self.radioButton.isChecked():
                        self.args = self.args + ' --html-output ' + self.dict['name'] + '.html'
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/' + self.dict['name'] + '.html'
                    if self.radioButton_2.isChecked():
                        self.args = self.args + ' --json-output ' + self.dict['name'] + '.txt'
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/'  + self.dict['name'] + '.txt'
                self.pushButton_3.setText("关闭主动扫描")
                self.process_creation()
                self.process.start(self.args)
            else:
                # 第二次按下按钮
                del self.is_first_click  # 删除标记
                self.pushButton_3.setText("开启主动扫描")
                self.textEdit.clear()
                self.process_kill()
        else:
            text = '未配置xray文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    # 开启被动扫描
    def passive_scan(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            if not hasattr(self, 'is_first_clicks'):
                if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
                    self.dict['name'] = str(int(time.time()))
                else:
                    self.dict['name'] = self.lineEdit_2.text()
                # 第一次按下按钮
                self.is_first_clicks = True
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    self.args = config['xray_address']
                    if self.radioButton_5.isChecked():
                        self.args = self.args + ' --log-level debug'
                    if self.radioButton_6.isChecked():
                        self.args = self.args + ' --log-level info'
                    if self.radioButton_7.isChecked():
                        self.args = self.args + ' --log-level warn'
                    if self.radioButton_8.isChecked():
                        self.args = self.args + ' --log-level error'
                    if self.radioButton_9.isChecked():
                        self.args = self.args + ' --log-level fatal'
                    self.args = self.args + ' webscan'
                    if self.radioButton_11.isChecked():
                        self.args = self.args + ' --level medium'
                    if self.radioButton_12.isChecked():
                        self.args = self.args + ' --level high'
                    if self.radioButton_13.isChecked():
                        self.args = self.args + ' --level critical'
                    if self.radioButton.isChecked():
                        self.args = self.args + ' --html-output ' + self.dict['name'] + '.html '
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/' + self.dict['name'] + '.html'
                    if self.radioButton_2.isChecked():
                        self.args = self.args + ' --json-output ' + self.dict['name'] + '.txt '
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/' + self.dict['name'] + '.txt'
                    self.args = self.args + '--listen ' + self.lineEdit_6.text() + ':' + self.lineEdit_7.text()
                self.pushButton_4.setText("关闭被动扫描")
                self.process_creation()
                self.process.start(self.args)
            else:
                # 第二次按下按钮
                del self.is_first_clicks  # 删除标记
                self.pushButton_4.setText("开启被动扫描")
                self.textEdit.clear()
                self.process_kill()
        else:
            text = '未配置xray文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    # 查看当前命令
    def command_look(self):
        if self.args:
            self.args = self.args.replace('--', '\n--')
            png = './img/成功.png'
            self.open_tishiwindow(self.args,png)
        else:
            text = '暂无命令'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    # 配置xray文件
    def xray_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*.exe);")
        self.lineEdit.setText(fileName)
        self.textEdit.clear()
        self.process_kill()
        if fileName:
            if os.path.exists('file_address.yaml'):
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    config['xray_address'] = fileName
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml.dump(config, file)
                self.process_creation()
                self.process.start(fileName)
            else:
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    yaml.dump({'xray_address': fileName}, file)
                    yaml.dump({'rad_address': None}, file)
                self.process_creation()
                self.process.start(fileName)
        # 判断是否有xray的config文件，没有则生成
        if not os.path.exists('config.yaml'):
            self.process.finished.connect(self.xray_start)


    def xray_start(self):
        self.textEdit.clear()
        self.process_kill()
        with open('file_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            self.process_creation()
            self.process.start(config['xray_address'])



    # 查看xray版本
    def xray_version(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            with open('file_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.process_creation()
                self.process.start(config['xray_address'])
        else:
            text = '未配置xray文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)


    # 创建cmd进程
    def process_creation(self):
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.handle_finished)

    # 命令输出
    def handle_output(self):
        try:
            data = self.process.readAll().data().decode('utf-8').strip()
            lines = data.split('\n')
            for line in lines:
                if "[INFO]" in line:
                    line = line.replace("[INFO]", f'<span style="color: blue;">[INFO]</span>')
                elif "[Vuln: dirscan]" in line:
                    line = line.replace("[Vuln: dirscan]", f'<span style="color: red;">[Vuln: dirscan]</span>')
                elif line.startswith('\t'):
                    line = f'<span style="color: purple;">&nbsp;&nbsp;&nbsp;&nbsp;{line}</span>'
                elif re.match(r'^[\u4e00-\u9fff]', line):
                    line = f'<span style="color: red;">{line}</span>'
                elif "requestSent" in line:
                    line = f'<span style="color: #FFBF00;">{line}</span>'
                elif "All pending" in line:
                    line = f'<span style="color: #00FF7F;">{line}</span>'
                self.textEdit.append(line)
        except:
            data = self.process.readAll().data().decode('latin-1').strip()
            lines = data.split('\n')
            for line in lines:
                if "[INFO]" in line:
                    line = line.replace("[INFO]", f'<span style="color: blue;">[INFO]</span>')
                elif "[Vuln: dirscan]" in line:
                    line = line.replace("[Vuln: dirscan]", f'<span style="color: red;">[Vuln: dirscan]</span>')
                elif line.startswith('\t'):
                    line = f'<span style="color: purple;">&nbsp;&nbsp;&nbsp;&nbsp;{line}</span>'
                elif re.match(r'^[\u4e00-\u9fff]', line):
                    line = f'<span style="color: red;">{line}</span>'
                elif "requestSent" in line:
                    line = f'<span style="color: #FFBF00;">{line}</span>'
                elif "All pending" in line:
                    line = f'<span style="color: #00FF7F;">{line}</span>'
                self.textEdit.append(line)

    # 当进程完成时，该方法会被调用。删除对象QProcess
    def handle_finished(self):
        self.process.deleteLater()
        self.process = None

    # 关闭进程
    def process_kill(self):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()  # 等待进程完全结束

    # 清空命令行输出
    def clear_cmd(self):
        self.textEdit.clear()
        self.process_kill()
        if hasattr(self, 'is_first_click'):
            del self.is_first_click
        if hasattr(self, 'is_first_clicks'):
            del self.is_first_clicks
        self.pushButton_3.setText("开启主动扫描")
        self.pushButton_4.setText("开启被动扫描")

    # 打开高级设置窗口
    def open_subwindow(self):
        if os.path.exists('config.yaml'):
            self.config_window = config.config_win()
            icon = QIcon('img/扫描.png')
            self.config_window.setWindowIcon(icon)
            self.config_window.show()
        else:
            text = '未配置xray文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    # 消息弹窗
    def open_tishiwindow(self,text,img):
        self.tishi_window = tishi.TiShi()
        icon = QIcon('img/扫描.png')
        self.tishi_window.setWindowIcon(icon)
        if text:
            self.tishi_window.label.setText(text)
        if img:
            self.tishi_window.label_2.setPixmap(QtGui.QPixmap(img))
        self.tishi_window.setWindowModality(Qt.ApplicationModal)  # 设置子窗口为应用程序模态
        self.tishi_window.show()



