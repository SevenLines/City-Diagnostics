import sys
import traceback
import typing
import ui.resources

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, QAbstractListModel, QModelIndex, Qt, QSaveFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from db import session
from models import Road
from reports import DiagnosticsReport
from ui.mainwindow import Ui_MainWindow


class RoadsModel(QAbstractListModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.roads = list(session.query(Road).order_by(Road.Name))

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.roads)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.roads[index.row()].Name

    def get_road(self, index):
        return self.roads[index]


class LogModel(QAbstractListModel):
    messages = []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.messages[index.row()][0]

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.messages)

    def clear(self):
        self.beginResetModel()
        self.messages = []
        self.endResetModel()

    def log(self, message, level):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.messages.insert(0, (message, level))
        self.endInsertRows()


class ReportWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    logged = QtCore.pyqtSignal(str, int)
    progressed = QtCore.pyqtSignal(int, int, str)

    def __init__(self, road: Road, save_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.road = road
        self.save_path = save_path

    @QtCore.pyqtSlot()
    def buildReport(self):
        try:
            report = DiagnosticsReport(self.road.id)
            report.progressed.connect(self.onProgress)
            doc = report.create()
            doc.save(self.save_path)
            self.finished.emit()
        except Exception as ex:
            self.logged.emit(traceback.format_exc(), 0)

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        self.progressed.emit(value, max, message)


class MainWindow(Ui_MainWindow, QMainWindow):
    thread = None
    roads_model = None
    path = "./out/"

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btnGenerate.clicked.connect(self.onGenerate)

        self.roads_model = RoadsModel()
        self.cmbRoad.setModel(self.roads_model)

        self.log_model = LogModel()
        self.lstMessages.setModel(self.log_model)

        movie = QtGui.QMovie(":images/loading.gif")
        movie.start()
        self.lblLoading.setVisible(False)
        self.lblLoading.setMovie(movie)

    def onGenerate(self):
        road = self.roads_model.get_road(self.cmbRoad.currentIndex())
        self.progressMain.setValue(0)
        self.log_model.clear()
        path = QFileDialog.getSaveFileName(directory="{}/{}.docx".format(self.path, road.Name))

        if path[0]:
            self.lblLoading.setVisible(True)
            self.btnGenerate.setDisabled(True)
            self.path = path[0]
            self.thread = QThread()
            self.worker = ReportWorker(road, self.path)
            self.worker.moveToThread(self.thread)
            self.worker.progressed.connect(self.onProgress)
            self.worker.finished.connect(self.onThreadFinished)
            self.worker.logged.connect(self.onLogged)
            self.thread.started.connect(self.worker.buildReport)
            self.thread.start()

    @QtCore.pyqtSlot(str, int)
    def onLogged(self, message, level):
        if level == 0:
            self.onThreadFinished()
        self.log_model.log(message, level)

    @QtCore.pyqtSlot()
    def onThreadFinished(self):
        self.lblLoading.setVisible(False)
        self.btnGenerate.setDisabled(False)
        self.thread.started.disconnect()
        self.worker.progressed.disconnect()
        self.worker.finished.disconnect()
        self.thread.exit()
        # self.thread = None
        # self.worker = None

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
