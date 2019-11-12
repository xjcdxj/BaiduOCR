from PyQt5 import QtWidgets
import sys

def copy():
    cl=QtWidgets.QApplication.clipboard()
    graph.setPixmap(cl.pixmap())
app=QtWidgets.QApplication(sys.argv)
ui=QtWidgets.QMainWindow()
graph=QtWidgets.QLabel(ui)
graph.resize(500,300)
burtton=QtWidgets.QPushButton(ui)
burtton.clicked.connect(copy)
ui.show()
sys.exit(app.exec_())
