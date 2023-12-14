import os
import ruamel.yaml
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon
from . import tishi
from .config_ui import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class config_win(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.setupUi(self)  
        self.process = None
        self.init_ui()
        self.tishi_window = None  

    def init_ui(self):
        '''
        插件配置:       checkBox_1 - checkBox_19
        baseline配置:  checkBox_20 - checkBox_30
        xss配置:       checkBox_31 - checkBox_32
        sqldet配置:    checkBox_33 - checkBox_37
        '''
        for i in range(1, 38):
            checkbox = getattr(self, f"checkBox_{i}")   
            self.checkboxes.append(checkbox)
        if os.path.exists('config.yaml'):
            self.initial()  
        else:
            self.process_kill()
            with open('xray_address.yaml', 'r', encoding='utf-8') as file:
                yaml = ruamel.yaml.YAML()
                config = yaml.load(file)
                try:
                    self.process_creation()
                    self.process.start(config['xray_address'])
                    self.process.finished.connect(self.initial)  
                except:
                    pass

        self.pushButton.clicked.connect(self.plug_recover)  
        self.pushButton_2.clicked.connect(self.plug_save)   
        self.pushButton_3.clicked.connect(self.baseline_recover)  
        self.pushButton_4.clicked.connect(self.baseline_save)  
        self.pushButton_7.clicked.connect(self.xss_recover)  
        self.pushButton_8.clicked.connect(self.xss_save)  
        self.pushButton_5.clicked.connect(self.sqldet_recover)  
        self.pushButton_6.clicked.connect(self.sqldet_save)  
        self.pushButton_10.clicked.connect(self.headers_save)   
        self.toolButton.clicked.connect(self.shiro_file)    
        self.pushButton_13.clicked.connect(self.shiro_save) 
        self.toolButton_2.clicked.connect(self.brute_username_file)  
        self.toolButton_3.clicked.connect(self.brute_password_file)  
        self.pushButton_11.clicked.connect(self.brute_force_save)  
        self.toolButton_4.clicked.connect(self.dirscan_file)  
        self.pushButton_12.clicked.connect(self.dirscan_save)  
        self.pushButton_14.clicked.connect(self.phantasm_save)  

        self.pushButton_9.clicked.connect(self.all_recover) 

    
    def initial(self):
        with open('dict/config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            
            for checkbox in self.checkboxes[0:19]:
                checkbox.setChecked(config['plugins'][checkbox.text()]['enabled'])
            for checkbox in self.checkboxes[19:30]:
                checkbox.setChecked(config['plugins']['baseline'][checkbox.text()])
            for checkbox in self.checkboxes[30:32]:
                checkbox.setChecked(config['plugins']['xss'][checkbox.text()])
            for checkbox in self.checkboxes[32:37]:
                checkbox.setChecked(config['plugins']['sqldet'][checkbox.text()])
            self.lineEdit.setText(config['http']['headers']['User-Agent'])
            if 'Cookie' in config['http']['headers']:
                self.lineEdit_2.setText(config['http']['headers']['Cookie'])
            else:
                
                self.lineEdit_2.setText("")  
            self.lineEdit_3.setText(config['plugins']['shiro']['cookie_name'])
            self.lineEdit_5.setText(config['plugins']['shiro']['aes_key_file'])
            self.lineEdit_6.setText(config['plugins']['brute-force']['username_dictionary'])
            self.lineEdit_7.setText(config['plugins']['brute-force']['password_dictionary'])
            self.lineEdit_8.setText(str(config['plugins']['dirscan']['depth']))
            self.lineEdit_9.setText(config['plugins']['dirscan']['dictionary'])
            self.lineEdit_10.setText(str(config['plugins']['phantasm']['depth']))

    
    def plug_recover(self):
        toggle_state = not self.checkboxes[0].isChecked()
        for checkbox in self.checkboxes[:19]:
            checkbox.setChecked(toggle_state)

    
    def plug_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        for checkbox in self.checkboxes[:19]:
            config['plugins'][checkbox.text()]['enabled'] = checkbox.isChecked()
        
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def baseline_recover(self):
        toggle_state = not self.checkboxes[19].isChecked()  
        for checkbox in self.checkboxes[19:30]:
            checkbox.setChecked(toggle_state)

    
    def baseline_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        for checkbox in self.checkboxes[19:30]:
            config['plugins']['baseline'][checkbox.text()] = checkbox.isChecked()
        
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def xss_recover(self):
        toggle_state = not self.checkboxes[30].isChecked()  
        for checkbox in self.checkboxes[30:32]:
            checkbox.setChecked(toggle_state)

    
    def xss_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        for checkbox in self.checkboxes[30:32]:
            config['plugins']['xss'][checkbox.text()] = checkbox.isChecked()
        
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def sqldet_recover(self):
        toggle_state = not self.checkboxes[32].isChecked()  
        for checkbox in self.checkboxes[32:37]:
            checkbox.setChecked(toggle_state)

    
    def sqldet_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        for checkbox in self.checkboxes[32:37]:
            config['plugins']['sqldet'][checkbox.text()] = checkbox.isChecked()
        
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def headers_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        config['http']['headers']['User-Agent'] = self.lineEdit.text()
        
        if self.lineEdit_2.text():
            config['http']['headers'].update({'Cookie': self.lineEdit_2.text()})
        else:
            config['http']['headers'].pop('Cookie', None)
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def shiro_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                   "All Files(*);")
        self.lineEdit_5.setText(fileName)

    
    def shiro_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        config['plugins']['shiro']['cookie_name'] = self.lineEdit_3.text()
        if self.lineEdit_4.text():  
            aes_keys = self.lineEdit_4.text().split(',')  
            config['plugins']['shiro']['aes_key'] = [key.strip() for key in aes_keys]  
        else:
            config['plugins']['shiro']['aes_key'] = []
        config['plugins']['shiro']['aes_key_file'] = self.lineEdit_5.text()
        
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def brute_username_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                   "All Files(*);")
        self.lineEdit_6.setText(fileName)

    
    def brute_password_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                   "All Files(*);")
        self.lineEdit_7.setText(fileName)

    
    def brute_force_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        config['plugins']['brute-force']['username_dictionary'] = self.lineEdit_6.text()
        config['plugins']['brute-force']['password_dictionary'] = self.lineEdit_7.text()
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def dirscan_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                   "All Files(*);")
        self.lineEdit_9.setText(fileName)

    
    def dirscan_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        if self.lineEdit_8.text().isdigit():    
            config['plugins']['dirscan']['depth'] = int(self.lineEdit_8.text())
        else:
            config['plugins']['dirscan']['depth'] = int(1)
        config['plugins']['dirscan']['dictionary'] = self.lineEdit_9.text()

        if self.textEdit.toPlainText():  
            aes_keys = self.textEdit.toPlainText().split(',')  
            config['plugins']['dirscan']['exclude_dir'] = [key.strip() for key in aes_keys]  
        else:
            config['plugins']['dirscan']['exclude_dir'] = []
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def phantasm_save(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
        
        if self.lineEdit_10.text().isdigit():  
            config['plugins']['phantasm']['depth'] = int(self.lineEdit_10.text())
        else:
            config['plugins']['phantasm']['depth'] = int(1)

        if self.textEdit_2.toPlainText():  
            aes_keys = self.textEdit_2.toPlainText().split(',')  
            config['plugins']['phantasm']['exclude_poc'] = [key.strip() for key in aes_keys]  
        else:
            config['plugins']['phantasm']['exclude_poc'] = []
        with open('config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)
        self.open_tishiwindow()

    
    def all_recover(self):
        self.process_kill()
        if os.path.exists('config.yaml'):
            os.remove('config.yaml')  
        with open('xray_address.yaml', 'r', encoding='utf-8') as file:
            yaml = ruamel.yaml.YAML()
            config = yaml.load(file)
            self.process_creation()
            self.process.start(config['xray_address'])  
        self.initial()
        self.open_tishiwindow()

    
    def open_tishiwindow(self):
        self.tishi_window = tishi.TiShi()
        icon = QIcon('img/扫描.png')
        self.tishi_window.setWindowIcon(icon)
        self.tishi_window.setWindowModality(Qt.ApplicationModal)  
        self.tishi_window.show()

    
    def process_creation(self):
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.handle_finished)

    
    def handle_output(self):
        pass

    
    def handle_finished(self):
        self.process.deleteLater()
        self.process = None

    
    def process_kill(self):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()  
