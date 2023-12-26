import base64
import binascii
import hashlib
import threading
import urllib.parse
from PyQt5.QtWidgets import QWidget
from .box3_ui import Ui_Form

class BOX3(QWidget,Ui_Form):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setupUi(self)  # 使用 sjui.Ui_Form 类中的方法初始化
        self.init_ui()
        self.connection_state = True  # 初始连接状态为加密

    def init_ui(self):
        self.pushButton.clicked.connect(self.toggle_1)
        self.pushButton_2.clicked.connect(self.toggle_2)
        self.textEdit.textChanged.connect(self.encrypt_txt)
        self.pushButton.setStyleSheet("background-color: #bbeeb9;")

    def toggle_1(self):
        if self.connection_state == False:
            self.pushButton.setStyleSheet("background-color: #bbeeb9;")
            self.pushButton_2.setStyleSheet("")
            self.textEdit.textChanged.disconnect(self.decode_txt)
            self.textEdit.textChanged.connect(self.encrypt_txt)
            self.connection_state = True
            self.encrypt_txt()

    def toggle_2(self):
        if self.connection_state == True:
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("background-color: #bbeeb9;")
            self.textEdit.textChanged.disconnect(self.encrypt_txt)
            self.textEdit.textChanged.connect(self.decode_txt)
            self.connection_state = False
            self.decode_txt()

    def start_encrypt_txt(self):
        t = threading.Thread(target=self.encrypt_txt)
        t.daemon = True
        t.start()

    def start_decode_txt(self):
        t = threading.Thread(target=self.decode_txt)
        t.daemon = True
        t.start()

    def encrypt_txt(self):
        str_txt = self.textEdit.toPlainText()
        # url编码
        self.textEdit_2.setText(urllib.parse.quote(str_txt))

        # Base64加密
        encoded_bytes = str_txt.encode('utf-8')
        base64_encoded = base64.b64encode(encoded_bytes)
        base64_string = base64_encoded.decode('utf-8')
        self.textEdit_3.setText(base64_string)

        # Hex编码
        encoded_bytes = str_txt.encode('utf-8')
        hex_encoded = binascii.hexlify(encoded_bytes)
        self.textEdit_4.setText(hex_encoded.decode('utf-8'))

        # 使用utf-8编码将字符串转换为字节串
        encoded_text = str_txt.encode('unicode_escape').decode('utf-8')
        self.textEdit_5.setText(encoded_text)

        #md5加密
        md5_hash = hashlib.md5()
        md5_hash.update(str_txt.encode('utf-8'))
        self.textEdit_6.setText(md5_hash.hexdigest())

    def decode_txt(self):
        str_txt = self.textEdit.toPlainText()
        # URL解码
        try:
            decoded_text = urllib.parse.unquote(str_txt)
            self.textEdit_2.setText(decoded_text)
        except:
            self.textEdit_2.setText('无法解密')

        # Base64解密
        try:
            base64_decoded = base64.b64decode(str_txt.encode('utf-8'))
            decoded_text = base64_decoded.decode('utf-8')
            self.textEdit_3.setText(decoded_text)
        except:
            self.textEdit_3.setText('无法解密')


        # Hex解码
        try:
            hex_decoded = binascii.unhexlify(str_txt.encode('utf-8'))
            decoded_text = hex_decoded.decode('utf-8')
            self.textEdit_4.setText(decoded_text)
        except:
            self.textEdit_4.setText('无法解密')

        # Unicode解码
        try:
            decoded_text = str_txt.encode('utf-8').decode('unicode_escape')
            self.textEdit_5.setText(decoded_text)
        except:
            self.textEdit_5.setText('无法解密')

        # md5撞库
        found_match = False  # 标记是否找到匹配的解密结果
        with open('./dict/top1w-md5.txt', 'r', encoding='utf-8') as fp:
            for line in fp:
                if str_txt == line.strip():
                    # 如果找到了匹配的MD5哈希值，我们可以从原始文件中获取相应的单词
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
