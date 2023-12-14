import os
import shutil
import time
import ruamel.yaml
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets, QtGui
from . import tishi, file_save
from .box2_ui import Ui_Form

class BOX2(QWidget,Ui_Form):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)  
        self.init_ui()
        self.process = None
        self.args = None
        self.dict = {'name':str(int(time.time())),'name_all':'','url':'','url2':''}

    def init_ui(self):
        self.initial()
        self.toolButton.clicked.connect(self.rad_file)    
        self.pushButton_10.clicked.connect(self.all_recover) 
        self.pushButton.clicked.connect(self.basics_save) 
        self.pushButton_2.clicked.connect(self.rad_version) 
        self.pushButton_3.clicked.connect(self.file_config) 
        self.pushButton_5.clicked.connect(self.command_look) 
        self.pushButton_4.clicked.connect(self.clear_cmd) 
        self.pushButton_6.clicked.connect(self.name_save) 
        self.pushButton_11.clicked.connect(self.rad_cookie) 
        self.lineEdit_3.textChanged.connect(self.url_save)  
        self.lineEdit_7.textChanged.connect(self.url2_save)  
        self.pushButton_8.clicked.connect(self.initiative_scan) 
        self.pushButton_9.clicked.connect(self.passive_scan) 
        self.pushButton_7.clicked.connect(self.file_look) 

    
    def initial(self):
        if os.path.exists('rad_config.yml'):
            with open('rad_config.yml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.spinBox.setValue(int(config['max_depth']))
                self.spinBox_2.setValue(int(config['navigate_timeout_second']))
                self.spinBox_3.setValue(int(config['max_interactive_depth']))
                self.spinBox_4.setValue(int(config['max_page_concurrent']))
                if 'Cookie' in config['domain_headers'][0]['headers']:
                    self.lineEdit_6.setText(config['domain_headers'][0]['headers']['Cookie'])
                else:
                    self.lineEdit_6.setText('')
        if os.path.exists('file_address.yaml'):
            with open('file_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.lineEdit.setText(config['rad_address'])

    
    def rad_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(), "All Files(*.exe);")
        self.lineEdit.setText(fileName)
        self.lineEdit.setText(fileName)
        self.textEdit.clear()
        self.process_kill()
        if fileName:
            if os.path.exists('file_address.yaml'):
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    config['rad_address'] = fileName
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml.dump(config, file)
                self.process_creation()
                self.process.start(fileName)
            else:
                with open('file_address.yaml', 'w', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    yaml.dump({'xray_address': None}, file)
                    yaml.dump({'rad_address': fileName}, file)
                self.process_creation()
                self.process.start(fileName)
        
        if not os.path.exists('rad_config.yml'):
            self.process.finished.connect(self.rad_start)

    def all_recover(self):
        if os.path.exists("./dict/rad_config.yml"):
            shutil.copy("./dict/rad_config.yml", 'rad_config.yml')
        self.initial()
        self.open_tishiwindow(None, None)

    
    def basics_save(self):
        if os.path.exists('file_address.yaml'):
            with open('rad_config.yml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                config['max_depth'] = int(self.spinBox.text())
                config['navigate_timeout_second'] = int(self.spinBox_2.text())
                config['max_interactive_depth'] = int(self.spinBox_3.text())
                config['max_page_concurrent'] = int(self.spinBox_4.text())
            with open('rad_config.yml', 'w', encoding='utf-8') as file:
                yaml.dump(config, file)
            self.open_tishiwindow(None, None)
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
    def rad_start(self):
        self.textEdit.clear()
        self.process_kill()
        with open('file_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            self.process_creation()
            self.process.start(config['rad_address'] + ' -t http://example.com')

    
    def rad_version(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            with open('file_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                self.process_creation()
                self.process.start(config['rad_address'])
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    def file_config(self):
        self.file_window = file_save.file_win()
        icon = QIcon('img/扫描.png')
        self.file_window.setWindowIcon(icon)
        self.rad_file_refresh()
        self.file_window.pushButton.clicked.connect(self.rad_file_refresh)    
        self.file_window.pushButton_2.clicked.connect(self.rad_file_save)  
        self.file_window.show()

    def rad_file_save(self):
        if os.path.exists('rad_config.yml'):
            yaml_text = self.file_window.textEdit.toPlainText()  
            with open('rad_config.yml', 'w', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(yaml_text)  
                yaml.dump(config, file)  
                text = '保存成功'
                img = './img/成功.png'
            self.open_tishiwindow(None, None)
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)


    def rad_file_refresh(self):
        with open('rad_config.yml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        output = ruamel.yaml.StringIO()
        yaml.dump(config, output)
        yaml_str = output.getvalue()
        self.file_window.textEdit.setText(yaml_str)

    
    def command_look(self):
        if self.args:
            self.args = self.args.replace('--', '\n--')
            png = './img/成功.png'
            self.open_tishiwindow(self.args, png)
        else:
            text = '暂无命令'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
    def name_save(self):
        if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
            self.dict['name'] = str(int(time.time()))
        else:
            self.dict['name'] = self.lineEdit_2.text()
        self.open_tishiwindow(None, None)

    
    def rad_cookie(self):
        if os.path.exists('file_address.yaml'):
            with open('rad_config.yml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                if self.lineEdit_6.text():
                    config['domain_headers'] = [{'domain': '*', 'headers': {'Cookie': self.lineEdit_6.text()}}]
                else:
                    config['domain_headers'] = [{'domain': '*', 'headers': {}}]
            with open('rad_config.yml', 'w', encoding='utf-8') as file:
                yaml.dump(config, file)
            self.open_tishiwindow(None, None)
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
    def url_save(self):
        self.dict['url'] = self.lineEdit_3.text()

    def url2_save(self):
        self.dict['url2'] = self.lineEdit_7.text()

    
    def initiative_scan(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            if not hasattr(self, 'is_first_click'):
                if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
                    self.dict['name'] = str(int(time.time()))
                else:
                    self.dict['name'] = self.lineEdit_2.text()
                
                self.is_first_click = True
                self.process_kill()
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    self.args = config['rad_address']
                    if self.dict['url']:
                        self.args = self.args + ' -t ' + self.dict['url']
                    if self.checkBox.isChecked():
                        self.args = self.args + ' --wait-login '
                    if self.radioButton.isChecked():
                        self.args = self.args + ' --text-output ' + self.dict['name'] + '.txt'
                        self.dict['name_all'] = os.path.dirname(config['rad_address']) + '/' + self.dict['name'] + '.txt'
                    if self.radioButton_2.isChecked():
                        self.args = self.args + ' --full-text-output ' + self.dict['name'] + '.txt'
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/'  + self.dict['name'] + '.txt'
                    if self.radioButton_3.isChecked():
                        self.args = self.args + ' --json-output ' + self.dict['name'] + '.json'
                        self.dict['name_all'] = os.path.dirname(config['xray_address']) + '/'  + self.dict['name'] + '.json'
                self.pushButton_8.setText("关闭主动扫描")
                self.process_creation()
                self.process.start(self.args)
                if self.checkBox.isChecked():
                    
                    reply = QMessageBox.question(self, '输入提示', '登录后请按确认', QMessageBox.Yes)
                    
                    if reply == QMessageBox.Yes:
                        self.process.write(b"\n")
            else:
                
                del self.is_first_click  
                self.pushButton_8.setText("开启主动扫描")
                self.textEdit.clear()
                self.process_kill()
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
    def passive_scan(self):
        if os.path.exists('file_address.yaml'):
            self.textEdit.clear()
            self.process_kill()
            if not hasattr(self, 'is_first_clicks'):
                if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == "默认则随机命名":
                    self.dict['name'] = str(int(time.time()))
                else:
                    self.dict['name'] = self.lineEdit_2.text()
                
                self.is_first_clicks = True
                with open('file_address.yaml', 'r', encoding='utf-8') as file:
                    yaml = ruamel.yaml.YAML()
                    config = yaml.load(file)
                    self.args = config['rad_address']
                    if self.dict['url']:
                        self.args = self.args + ' -t ' + self.dict['url2']
                    self.args = self.args + ' -http-proxy ' + self.lineEdit_4.text() + ':' + self.lineEdit_5.text()
                self.pushButton_9.setText("关闭被动扫描")
                self.process_creation()
                self.process.start(self.args)
                print(self.args)
            else:
                
                del self.is_first_clicks  
                self.pushButton_9.setText("开启被动扫描")
                self.textEdit.clear()
                self.process_kill()
        else:
            text = '未配置rad文件'
            img = './img/失败.png'
            self.open_tishiwindow(text, img)

    
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
        self.pushButton_8.setText("开启主动扫描")
        self.pushButton_9.setText("开启被动扫描")

    
    def open_tishiwindow(self, text, img):
        self.tishi_window = tishi.TiShi()
        icon = QIcon('img/扫描.png')
        self.tishi_window.setWindowIcon(icon)
        if text:
            self.tishi_window.label.setText(text)
        if img:
            self.tishi_window.label_2.setPixmap(QtGui.QPixmap(img))
        self.tishi_window.setWindowModality(Qt.ApplicationModal)  
        self.tishi_window.show()