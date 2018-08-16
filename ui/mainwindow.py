# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 410)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ediFilter = QtWidgets.QLineEdit(self.centralwidget)
        self.ediFilter.setObjectName("ediFilter")
        self.verticalLayout.addWidget(self.ediFilter)
        self.lstRoads = QtWidgets.QListView(self.centralwidget)
        self.lstRoads.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstRoads.setObjectName("lstRoads")
        self.verticalLayout.addWidget(self.lstRoads)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblLoading = QtWidgets.QLabel(self.centralwidget)
        self.lblLoading.setText("")
        self.lblLoading.setTextFormat(QtCore.Qt.AutoText)
        self.lblLoading.setObjectName("lblLoading")
        self.horizontalLayout.addWidget(self.lblLoading)
        self.progressMain = QtWidgets.QProgressBar(self.centralwidget)
        self.progressMain.setProperty("value", 0)
        self.progressMain.setAlignment(QtCore.Qt.AlignCenter)
        self.progressMain.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressMain.setObjectName("progressMain")
        self.horizontalLayout.addWidget(self.progressMain)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.btnGenerate = QtWidgets.QPushButton(self.centralwidget)
        self.btnGenerate.setObjectName("btnGenerate")
        self.horizontalLayout.addWidget(self.btnGenerate)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.txtLog = QtWidgets.QTextEdit(self.centralwidget)
        self.txtLog.setObjectName("txtLog")
        self.gridLayout.addWidget(self.txtLog, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Диагностика отчеты"))
        self.progressMain.setFormat(_translate("MainWindow", "%p%"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Сгенерировать docx (диагностика)"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Сгенерировать docx (ровность)"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Сгенерировать карты (*.png)"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Сгенерировать json"))
        self.btnGenerate.setText(_translate("MainWindow", "Запуск"))

