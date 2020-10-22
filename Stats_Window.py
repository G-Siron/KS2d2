# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Stats_Window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(791, 750)
        self.textEdit_Stats = QtWidgets.QTextEdit(Form)
        self.textEdit_Stats.setGeometry(QtCore.QRect(10, 10, 771, 701))
        self.textEdit_Stats.setObjectName("textEdit_Stats")
        self.pushButton_saveStats = QtWidgets.QPushButton(Form)
        self.pushButton_saveStats.setGeometry(QtCore.QRect(10, 715, 114, 32))
        self.pushButton_saveStats.setObjectName("pushButton_saveStats")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_saveStats.setText(_translate("Form", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

