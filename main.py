from window import Ui_MainWindow
from base import ocr_token
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, json, base64
from urllib import request, parse
from threading import Thread


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('文字识别')
        self.image = None
        self.lineEdit.setText('输入图片地址')
        self.textBrowser.setText('百度OCR')
        self.binding()

    def binding(self):
        self.start_button.clicked.connect(self.parse)
        self.pushButton.clicked.connect(self.parse)
        self.signal.connect(self.warn)

    def choose_img(self):
        self.image = QtWidgets.QFileDialog.getOpenFileName(self, '.')[0]
        self.lineEdit.setText(self.image)

    def warn(self, info):
        self.textBrowser.setText(info)

    def parse(self):
        sender = self.sender()
        if sender == self.start_button:
            if not self.lineEdit.text().endswith('jpg' and 'png'):
                QtWidgets.QMessageBox.warning(self, '警告', '图片错误', QtWidgets.QMessageBox.Ok)
            else:
                t = Thread(target=self.start, args=())
                t.start()

        elif sender == self.pushButton:
            self.choose_img()

    def start(self):
        self.signal.emit('识别中。。。')
        token = ocr_token()
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        with open(self.image, 'rb') as f:
            image = f.read()
        image = base64.b64encode(image)
        data = {
            'access_token': token,
            'image': image
        }
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = parse.urlencode(data).encode('utf-8')
        rq = request.Request(url, headers=header, data=data)
        response = request.urlopen(rq)
        result = response.read().decode()
        result = json.loads(result)['words_result']
        self.signal.emit('')
        text = ''
        for i in result:
            text = text + i['words'] + '\n'
            # self.textBrowser.append(i['words'] + '\n')
        self.signal.emit(text)
        # print(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
