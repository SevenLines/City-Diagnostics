import sys
import traceback
from time import sleep

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow

from reports import DiagnosticsReport
from ui.mainwindow import Ui_MainWindow


class ReportWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progressed = QtCore.pyqtSignal(int, int, str)

    @QtCore.pyqtSlot()
    def buildReport(self):
        report = DiagnosticsReport(5)
        report.progressed.connect(self.onProgress)
        doc = report.create()
        doc.save("out.docx")
        self.finished.emit()

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        self.progressed.emit(value, max, message)


class MainWindow(Ui_MainWindow, QMainWindow):
    thread = None

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btnGenerate.clicked.connect(self.onGenerate)

    def onGenerate(self):
        if not self.thread:
            self.thread = QThread()
            self.worker = ReportWorker()
            self.worker.moveToThread(self.thread)
            self.worker.progressed.connect(self.onProgress)
            self.worker.finished.connect(self.onThreadFinished)
            self.thread.started.connect(self.worker.buildReport)
            self.thread.start()

    @QtCore.pyqtSlot()
    def onThreadFinished(self):
        self.thread = None
        self.worker = None

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        self.progressMain.setMaximum(max)
        self.progressMain.setValue(value)
        self.progressMain.setFormat("{} %p%".format(message))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

