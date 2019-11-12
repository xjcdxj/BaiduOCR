import base64
import json
import os
import re
import sys
from threading import Thread
from urllib import parse, request

from PyQt5 import QtCore, QtWidgets

from base import ocr_token
from window import Ui_MainWindow


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('文字识别')
        self.image = None
        self.text = ''
        self.lineEdit.setText('输入图片地址')
        self.setAcceptDrops(True)
        # self.textBrowser.setText('百度OCR')
        self.binding()

    def dragEnterEvent(self, env):
        if re.match(r'.+\.(jpg|png|tif|bmp)', env.mimeData().text()):
            # print('kk')
            env.accept()
            self.statusbar.showMessage("Release Mouse")
        else:
            self.statusbar.showMessage("Format Unsupported")
            env.ignore()

        pass

    def dropEvent(self, env):
        self.lineEdit.setText(re.match(r'file:///(.+\.(jpg|png|tif|bmp))', env.mimeData().text()).groups()[0])

    def dragMoveEvent(self, env):
        self.statusbar.showMessage("Release mouse")
        pass

    def binding(self):
        self.start_button.clicked.connect(self.parse)
        self.pushButton.clicked.connect(self.parse)
        self.signal.connect(self.warn)
        # self.textBrowser.mouseDoubleClickEvent()
        self.textBrowser.customContextMenuRequested.connect(self.rightClicked)
        self.textBrowser.setToolTip("右键复制内容")

    def rightClicked(self):
        # print(self.textBrowser.text())
        QtWidgets.QApplication.clipboard().setText(self.text)
        pass

    def choose_img(self):
        self.image = QtWidgets.QFileDialog.getOpenFileName(self, '.')[0]
        self.lineEdit.setText(self.image)

    def warn(self, status, info):
        if status == 'information':
            self.statusbar.showMessage(info)
        elif status == 'warning':
            QtWidgets.QMessageBox.information(
                self, ' 提示', info, QtWidgets.QMessageBox.Ok)
        elif status == 'show':
            print(info)
            self.textBrowser.setText(info)

    def parse(self):
        sender = self.sender()
        if sender == self.start_button:
            if os.path.exists(self.lineEdit.text()):
                if not re.match(r'.+\.(jpg|png)', self.lineEdit.text()):
                    QtWidgets.QMessageBox.warning(
                        self, '警告', '图片错误', QtWidgets.QMessageBox.Ok)
                else:
                    t = Thread(target=self.start, args=())
                    t.start()
            else:
                QtWidgets.QMessageBox.warning(
                    self, '警告', '文件不存在', QtWidgets.QMessageBox.Ok)

        elif sender == self.pushButton:
            self.choose_img()

    def start(self):
        self.signal.emit('information', '识别中。。。')
        token = ocr_token()
        if token[0] == 1:
            self.signal.emit('warning', token[1])
            exit()
        self.token = token[1]
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        try:
            with open(self.lineEdit.text(), 'rb') as f:
                image = f.read()
            image = base64.b64encode(image)
        except FileNotFoundError:
            self.signal.emit('warning', '未找到图片！')
            exit()
        if len(image) > 4 * 1024 * 1024:
            self.signal.emit('warning', '图片大小超过4MB')
            exit()

        data = {
            'access_token': self.token,
            'image': image
        }
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = parse.urlencode(data).encode('utf-8')
        rq = request.Request(url, headers=header, data=data)
        response = request.urlopen(rq)
        result = response.read().decode()
        try:
            result = json.loads(result)['words_result']
            if not result:
                self.signal.emit('warning', '未识别出文字。')
            else:
                # print(result)
                self.statusbar.showMessage('识别成功')
                # self.textBrowser.append('*' * len(self.lineEdit.text()))
                # self.textBrowser.append(self.lineEdit.text() + '\n')
                self.text = ''
                for i in result:
                    self.text = self.text + i['words'] + '\n'
                self.signal.emit('show', self.text)

                # print(text)
                # self.textBrowser.append(i['words'] + '\n')
                # self.textBrowser.append('*' * len(self.lineEdit.text()) + '\n')
        except KeyError:
            self.signal.emit('warning', '失败！！！')

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
