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
        self.cmbRoad = QtWidgets.QComboBox(self.centralwidget)
        self.cmbRoad.setObjectName("cmbRoad")
        self.verticalLayout.addWidget(self.cmbRoad)
        self.btnGenerate = QtWidgets.QPushButton(self.centralwidget)
        self.btnGenerate.setObjectName("btnGenerate")
        self.verticalLayout.addWidget(self.btnGenerate)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressMain = QtWidgets.QProgressBar(self.centralwidget)
        self.progressMain.setProperty("value", 0)
        self.progressMain.setAlignment(QtCore.Qt.AlignCenter)
        self.progressMain.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressMain.setObjectName("progressMain")
        self.horizontalLayout.addWidget(self.progressMain)
        self.lblLoading = QtWidgets.QLabel(self.centralwidget)
        self.lblLoading.setText("")
        self.lblLoading.setPixmap(QtGui.QPixmap("images/loading.gif"))
        self.lblLoading.setObjectName("lblLoading")
        self.horizontalLayout.addWidget(self.lblLoading)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.lstMessages = QtWidgets.QListView(self.centralwidget)
        self.lstMessages.setObjectName("lstMessages")
        self.gridLayout.addWidget(self.lstMessages, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 531, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Диагностика отчеты"))
        self.btnGenerate.setText(_translate("MainWindow", "Сгенерировать"))
        self.progressMain.setFormat(_translate("MainWindow", "%p%"))

