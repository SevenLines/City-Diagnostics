# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(531, 410)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ediFilter = QLineEdit(self.centralwidget)
        self.ediFilter.setObjectName(u"ediFilter")

        self.verticalLayout.addWidget(self.ediFilter)

        self.lstRoads = QListView(self.centralwidget)
        self.lstRoads.setObjectName(u"lstRoads")
        self.lstRoads.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.lstRoads)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblLoading = QLabel(self.centralwidget)
        self.lblLoading.setObjectName(u"lblLoading")
        self.lblLoading.setTextFormat(Qt.AutoText)

        self.horizontalLayout.addWidget(self.lblLoading)

        self.progressMain = QProgressBar(self.centralwidget)
        self.progressMain.setObjectName(u"progressMain")
        self.progressMain.setValue(0)
        self.progressMain.setAlignment(Qt.AlignCenter)
        self.progressMain.setTextDirection(QProgressBar.TopToBottom)

        self.horizontalLayout.addWidget(self.progressMain)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.btnGenerate = QPushButton(self.centralwidget)
        self.btnGenerate.setObjectName(u"btnGenerate")

        self.horizontalLayout.addWidget(self.btnGenerate)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.txtLog = QTextEdit(self.centralwidget)
        self.txtLog.setObjectName(u"txtLog")

        self.gridLayout.addWidget(self.txtLog, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0430\u0433\u043d\u043e\u0441\u0442\u0438\u043a\u0430 \u043e\u0442\u0447\u0435\u0442\u044b", None))
        self.lblLoading.setText("")
        self.progressMain.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0434\u0438\u0430\u0433\u043d\u043e\u0441\u0442\u0438\u043a\u0430)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0448\u0435\u043b\u0435\u0445\u043e\u0432)", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0440\u043e\u0432\u043d\u043e\u0441\u0442\u044c)", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0443\u0447\u0430\u0441\u0442\u043a\u043e\u0432 \u0432 \u0431\u0430\u043b\u043b\u0430\u0445)", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0435 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f)", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c docx (\u0447\u0438\u0442\u0430 2023)", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043a\u0430\u0440\u0442\u044b (*.png)", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c json", None))

        self.btnGenerate.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
    # retranslateUi

