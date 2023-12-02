import os
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
        self.setupUi(self)  
        self.init_ui()
        self.config_window = None
        self.process = None
        self.args = None
        self.dict = {'name':str(int(time.time())),'name_all':'','url':'','request':'','url_list':''}

    def init_ui(self):
        self.initial()
        self.pushButton_8.clicked.connect(self.open_subwindow)
        self.toolButton.clicked.connect(self.xray_file)         
        self.pushButton.clicked.connect(self.basics_save)       
        self.pushButton_6.clicked.connect(self.clear_cmd)       
        self.pushButton_5.clicked.connect(self.xray_version)    
        self.pushButton_2.clicked.connect(self.name_save)       
        self.lineEdit_3.textChanged.connect(self.url_save)      
        self.toolButton_2.clicked.connect(self.request_body)    
        self.toolButton_3.clicked.connect(self.url_list_save)   
        self.pushButton_3.clicked.connect(self.initiative_scan) 
        self.pushButton_4.clicked.connect(self.passive_scan)    
        self.pushButton_9.clicked.connect(self.file_look)       
        self.pushButton_10.clicked.connect(self.command_look)   
        self.pushButton_7.clicked.connect(self.poc_start)       

    
    def initial(self):
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.spinBox.setValue(int(config['parallel']))
                self.spinBox_2.setValue(int(config['http']['dial_timeout']))
                self.spinBox_3.setValue(int(config['http']['max_redirect']))
                self.spinBox_4.setValue(int(config['http']['max_qps']))
        if os.path.exists('xray_address.yaml'):
            with open('xray_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.lineEdit.setText(config['xray_address'])

    
    def basics_save(self):
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


    
    def name_save(self):
        if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
            self.dict['name'] = str(int(time.time()))
        else:
            self.dict['name'] = self.lineEdit_2.text()
        self.open_tishiwindow(None, None)

    
    def poc_start(self):
        url = QtCore.QUrl('https://poc.xray.cool/')
        QtGui.QDesktopServices.openUrl(url)

    
    def url_save(self):
        self.dict['url']=self.lineEdit_3.text()
        self.dict['request']=''
        self.dict['url_list']=''
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

    
    def request_body(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);")
        self.dict['url'] = ''
        self.dict['request'] = fileName
        self.dict['url_list'] = ''
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText(fileName)
        self.lineEdit_5.setText('')

    
    def url_list_save(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*);")
        self.dict['url'] = ''
        self.dict['request'] = ''
        self.dict['url_list'] = fileName
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText(fileName)

    
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

    
    def initiative_scan(self):
        self.textEdit.clear()
        self.process_kill()
        if not hasattr(self, 'is_first_click'):
            
            self.is_first_click = True
            self.process_kill()
            with open('xray_address.yaml', 'r', encoding='utf-8') as file:
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
            
            del self.is_first_click  
            self.pushButton_3.setText("开启主动扫描")
            self.textEdit.clear()
            self.process_kill()

    
    def passive_scan(self):
        self.textEdit.clear()
        self.process_kill()
        if not hasattr(self, 'is_first_clicks'):
            
            self.is_first_clicks = True
            with open('xray_address.yaml', 'r', encoding='utf-8') as file:
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
            
            del self.is_first_clicks  
            self.pushButton_4.setText("开启被动扫描")
            self.textEdit.clear()
            self.process_kill()

    
    def command_look(self):
        if self.args:
            self.args = self.args.replace('--', '\n--')
            png = './img/成功.png'
            self.open_tishiwindow(self.args,png)
        else:
            text = '暂无命令'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
    def xray_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*.exe);")
        self.lineEdit.setText(fileName)
        if fileName:
            with open('xray_address.yaml', 'w', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                yaml.dump({'xray_address': fileName}, file)
            
            self.process_creation()
            self.process.start(fileName)

    
    def xray_version(self):
        self.textEdit.clear()
        self.process_kill()
        with open('xray_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            self.process_creation()
            self.process.start(config['xray_address'])

    
    def process_creation(self):
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.handle_finished)

    
    def handle_output(self):
        try:
            data = self.process.readAll().data().decode('utf-8').rstrip()
            
            self.textEdit.append(data)
        except:
            data = self.process.readAll().data().decode('latin-1').rstrip()
            
            self.textEdit.append(data)

    
    def handle_finished(self):
        self.process.deleteLater()
        self.process = None

    
    def process_kill(self):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()  

    
    def clear_cmd(self):
        self.textEdit.clear()
        self.process_kill()
        if hasattr(self, 'is_first_click'):
            del self.is_first_click
        if hasattr(self, 'is_first_clicks'):
            del self.is_first_clicks
        self.pushButton_3.setText("开启主动扫描")
        self.pushButton_4.setText("开启被动扫描")

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

    
    def open_tishiwindow(self,text,img):
        self.tishi_window = tishi.TiShi()
        icon = QIcon('img/扫描.png')
        self.tishi_window.setWindowIcon(icon)
        if text:
            self.tishi_window.label.setText(text)
        if img:
            self.tishi_window.label_2.setPixmap(QtGui.QPixmap(img))
        self.tishi_window.setWindowModality(Qt.ApplicationModal)  
        self.tishi_window.show()



