import os
import sys
import traceback
import typing

from PyQt5.QtGui import QBrush

import ui.resources

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, QAbstractListModel, QModelIndex, Qt, QSaveFile, QRunnable, QThreadPool, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QItemDelegate, QStyledItemDelegate

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
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3

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


class ReportWorkerSignals(QObject):
    finished = QtCore.pyqtSignal(object)
    logged = QtCore.pyqtSignal(str, int)
    progressed = QtCore.pyqtSignal(int, int, str)

    def __init__(self, road, *args, **kwargs) -> None:
        super(ReportWorkerSignals, self).__init__(*args, **kwargs)
        self.road = road

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        self.progressed.emit(value, max, "{}: {}".format(self.road.Name, message))


class ReportWorker(QRunnable):

    def __init__(self, road: Road, save_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.road = road
        self.save_path = save_path
        self.signals = ReportWorkerSignals(self.road)

    def run(self):
        try:
            self.signals.logged.emit("Обработка {}".format(self.road.Name), LogModel.INFO)
            report = DiagnosticsReport(self.road.id)
            report.progressed.connect(self.signals.onProgress)
            doc = report.create()
            doc.save(self.save_path)
            self.signals.finished.emit(self)
        except Exception as ex:
            self.signals.logged.emit("{}:{}".format(self.road.Name, traceback.format_exc()), LogModel.ERROR)


class MainWindow(Ui_MainWindow, QMainWindow):
    thread = None
    roads_model = None
    path = "./out/"
    workers = []

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btnGenerate.clicked.connect(self.onGenerate)

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(8)

        self.roads_model = RoadsModel()
        self.lstRoads.setModel(self.roads_model)

        self.log_model = LogModel()
        self.lstMessages.setModel(self.log_model)

        movie = QtGui.QMovie(":images/loading.gif")
        movie.start()
        self.lblLoading.setVisible(False)
        self.lblLoading.setMovie(movie)

    def onGenerate(self):
        roads = self.lstRoads.selectedIndexes()
        self.log_model.clear()
        path = QFileDialog.getExistingDirectory(directory="{}/".format(self.path))
        if path:
            self.progressMain.setMaximum(len(roads))
            self.progressMain.setValue(0)
            self.lblLoading.setVisible(True)
            for r in roads:
                road = self.roads_model.get_road(r.row())
                worker = ReportWorker(road, os.path.join(path, "{}.docx".format(road.Name)))
                worker.signals.logged.connect(self.onLogged)

                worker.signals.finished.connect(self.onReportFinished)
                self.workers.append(worker)
                self.pool.start(worker)

    @QtCore.pyqtSlot(str, int)
    def onLogged(self, message, level):
        if level == LogModel.ERROR:
            self.progressMain.setValue(self.progressMain.value() + 1)
            if self.progressMain.value() == self.progressMain.maximum():
                self.lblLoading.setVisible(False)

        self.log_model.log(message, level)

    @QtCore.pyqtSlot(object)
    def onReportFinished(self, report):
        self.progressMain.setValue(self.progressMain.value() + 1)
        if self.progressMain.value() == self.progressMain.maximum():
            self.lblLoading.setVisible(False)
        self.log_model.log("\"{}\" готова".format(report.road.Name), 1)

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
