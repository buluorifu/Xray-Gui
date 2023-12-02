import base64
import binascii
import hashlib
import urllib.parse
from PyQt5.QtWidgets import QWidget
from .box2_ui import Ui_Form

class BOX2(QWidget,Ui_Form):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)  
        self.init_ui()

    def init_ui(self):

        self.pushButton_2.clicked.connect(self.encrypt_txt)
        self.pushButton.clicked.connect(self.decode_txt)
        self.textEdit.textChanged.connect(self.encrypt_txt)

    def encrypt_txt(self):
        str_txt = self.textEdit.toPlainText()
        
        self.textEdit_2.setText(urllib.parse.quote(str_txt))

        
        encoded_bytes = str_txt.encode('utf-8')
        base64_encoded = base64.b64encode(encoded_bytes)
        base64_string = base64_encoded.decode('utf-8')
        self.textEdit_3.setText(base64_string)

        
        encoded_bytes = str_txt.encode('utf-8')
        hex_encoded = binascii.hexlify(encoded_bytes)
        self.textEdit_4.setText(hex_encoded.decode('utf-8'))

        
        encoded_text = str_txt.encode('unicode_escape').decode('utf-8')
        self.textEdit_5.setText(encoded_text)

        
        md5_hash = hashlib.md5()
        md5_hash.update(str_txt.encode('utf-8'))
        self.textEdit_6.setText(md5_hash.hexdigest())

    def decode_txt(self):
        str_txt = self.textEdit.toPlainText()
        
        try:
            decoded_text = urllib.parse.unquote(str_txt)
            self.textEdit_2.setText(decoded_text)
        except:
            self.textEdit_2.setText('无法解密')

        
        try:
            base64_decoded = base64.b64decode(str_txt.encode('utf-8'))
            decoded_text = base64_decoded.decode('utf-8')
            self.textEdit_3.setText(decoded_text)
        except:
            self.textEdit_3.setText('无法解密')


        
        try:
            hex_decoded = binascii.unhexlify(str_txt.encode('utf-8'))
            decoded_text = hex_decoded.decode('utf-8')
            self.textEdit_4.setText(decoded_text)
        except:
            self.textEdit_4.setText('无法解密')

        
        try:
            decoded_text = str_txt.encode('utf-8').decode('unicode_escape')
            self.textEdit_5.setText(decoded_text)
        except:
            self.textEdit_5.setText('无法解密')

        
        found_match = False  
        with open('./dict/top1w-md5.txt', 'r', encoding='utf-8') as fp:
            for line in fp:
                if str_txt in line:
                    
                    with open("./dict/top1w.txt", 'r', encoding='utf-8') as wp:
                        for word_line in wp:
                            words = word_line.split()
                            for word in words:
                                if hashlib.md5(word.encode('utf-8')).hexdigest() == str_txt:
                                    found_match = True
                                    self.textEdit_6.setText(word)
                                    break
                            if found_match:
                                break
        if not found_match:
            self.textEdit_6.setText('无法解密')