import json
import os
import sys
import traceback
import typing

import cairo
import docx
import geo2image
import math
import mercantile

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QRunnable, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog

from db import session, Session
from helpers import add_row
from models import Road
from reports import DiagnosticsReport, get_km
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

    def __init__(self, road=None, *args, **kwargs) -> None:
        super(ReportWorkerSignals, self).__init__(*args, **kwargs)
        self.road = road

    @QtCore.pyqtSlot(int, int, str)
    def onProgress(self, value, max, message):
        self.progressed.emit(value, max, "{}: {}".format(self.road.Name if self.road else '', message))


class ReportWorker(QRunnable):
    def __init__(self, road: Road, save_path: str,
                 as_json=False,
                 quality_only=False,
                 smooth_only=False,
                 correspondence_only=False,
                 shelehov=False,
                 default_category="4",
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.road = road
        self.save_path = save_path
        self.as_json = as_json
        self.shelehov = shelehov
        self.default_category = default_category
        self.smooth_only = smooth_only
        self.correspondence_only = correspondence_only
        self.quality_only = quality_only
        self.signals = ReportWorkerSignals(self.road)

    def run(self):
        try:
            self.signals.logged.emit("Обработка {}".format(self.road.Name), LogModel.INFO)
            report = DiagnosticsReport(self.road.id, default_category=self.default_category)
            report.progressed.connect(self.signals.onProgress)
            if self.as_json:
                data = report.create_json()
                with open(self.save_path, 'w') as f:
                    json.dump({
                        self.road.id: data
                    }, f)
            elif self.smooth_only:
                doc = report.create_smooth_only()
                doc.save(self.save_path)
            elif self.quality_only:
                doc = report.create_quality_only()
                doc.save(self.save_path)
            elif self.correspondence_only:
                doc = report.create_correspondence_only()
                doc.save(self.save_path)
            elif self.shelehov:
                doc = report.create_shelehov()
                doc.save(self.save_path)
            else:
                doc = report.create()
                doc.save(self.save_path)
            report.close()
            self.signals.finished.emit(self)
        except Exception as ex:
            self.signals.logged.emit("{}:{}".format(self.road.Name, traceback.format_exc()), LogModel.ERROR)


class MapImageWorker(QRunnable):
    def __init__(self, road: Road, save_path: str, zoom:int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.road = road
        self.save_path = save_path
        self.zoom = zoom
        self.signals = ReportWorkerSignals(self.road)
        self.session = Session()

    def run(self):
        try:
            self.signals.logged.emit("Обработка {}".format(self.road.Name), LogModel.INFO)
            points = self.road.get_main_axe_coordinates(self.session)
            west = min(p['lng'] for p in points)
            east = max(p['lng'] for p in points)
            south = min(p['lat'] for p in points)
            north = max(p['lat'] for p in points)
            img = geo2image.GeoImage(west, south, east, north, self.zoom, pool_workers=4)
            img.update()

            with img.cairo_surface() as surface:
                context = cairo.Context(surface)
                with img.cairo_matrix_override(context):
                    context.set_source_rgb(1, 0.2, 0.2)
                    x, y = mercantile.xy(points[0]['lng'], points[0]['lat'])
                    context.arc(x, y, 11 / img.kx, 0, math.pi * 2)
                    context.fill()

                    context.set_source_rgb(1, 0.2, 0.2)
                    x, y = mercantile.xy(points[-1]['lng'], points[-1]['lat'])
                    context.arc(x, y, 11 / img.kx, 0, math.pi * 2)
                    context.fill()

                    context.set_source_rgba(1, 0.2, 0.2, 0.4)
                    context.set_line_width(10 / img.kx)
                    for p in points:
                        x,y = mercantile.xy(p['lng'], p['lat'])
                        context.line_to(x, y)
                    context.stroke()
                surface.write_to_png(self.save_path)
            self.signals.finished.emit(self)
        except Exception as ex:
            self.signals.logged.emit("{}:{}".format(self.road.Name, traceback.format_exc()), LogModel.ERROR)
        finally:
            self.session.close()


class MainWindow(Ui_MainWindow, QMainWindow):
    thread = None
    roads_model = None
    path = "./out/"
    zoom = 11
    default_category = '4'
    workers = []

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btnGenerate.clicked.connect(self.onGenerate)

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(8)

        self.roads_model = RoadsModel()
        self.lstRoads.setModel(self.roads_model)

        movie = QtGui.QMovie(":images/loading.gif")
        movie.start()
        self.lblLoading.setVisible(False)
        self.lblLoading.setMovie(movie)

    def _generate(self, road_processor):
        roads = self.lstRoads.selectedIndexes()
        self.txtLog.clear()
        path = QFileDialog.getExistingDirectory(directory="{}/".format(self.path))
        if path:
            self.path = path
            self.progressMain.setMaximum(len(roads))
            self.progressMain.setValue(0)
            self.btnGenerate.setDisabled(True)
            self.lblLoading.setVisible(True)
            for r in roads:
                road = self.roads_model.get_road(r.row())
                worker = road_processor(road, path)
                worker.signals.logged.connect(self.onLogged)
                worker.signals.finished.connect(self.onReportFinished)
                self.workers.append(worker)
                self.pool.start(worker)

    def generate_json(self):
        def json_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.json".format(
                    road.Name[:100].replace("\"", "").replace("/", "-"))), as_json=True)

        return self._generate(json_road_processor)

    def generate_docx_smooth(self):
        def docx_smooth_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.docx".format(
                    road.Name[:100].replace("\"", "").replace("/", "-"))), smooth_only=True)
        return self._generate(docx_smooth_road_processor)

    def generate_docx(self):
        def docx_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.docx".format(
                    road.Name[:100].replace("\"", "").replace("/", "-"))))

        return self._generate(docx_road_processor)

    def generate_docx_shelehov(self):
        def docx_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.docx".format(
                    road.Name[:100].replace("\"", "").replace("/", "-"))), shelehov=True)

        return self._generate(docx_road_processor)

    def generate_png(self):
        zoom, cancel = QInputDialog.getInt(self, "Введите желаемый зум для карты", "Зум карты", self.zoom)
        if not cancel:
            return
        self.zoom = zoom

        def png_road_processor(road, path):
            return MapImageWorker(
                    road,
                    os.path.join(path, "{}.png".format(road.Name[:100].replace("\"", "").replace("/", "-"))),
                    zoom=zoom
                )

        return self._generate(png_road_processor)

    def generate_quality_report(self):
        def docx_quality_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.docx".format(
                    road.Name[:100].replace("\"", "").replace("/", "-"))), quality_only=True)
        return self._generate(docx_quality_road_processor)

    def generate_docx_conformity(self):
        category, cancel = QInputDialog.getText(self, "Введите категорию по умолчанию", "Категория",
                                                text=self.default_category)
        if not cancel:
            return
        self.default_category = category

        def docx_quality_road_processor(road, path):
            return ReportWorker(road, os.path.join(path, "{}.docx".format(
                road.Name[:100].replace("\"", "").replace("/", "-"))),
                                correspondence_only=True,
                                default_category=self.default_category)
        return self._generate(docx_quality_road_processor)

    def onGenerate(self):
        if self.comboBox.currentText() == 'Сгенерировать docx (диагностика)':
            self.generate_docx()
        elif self.comboBox.currentText() == 'Сгенерировать docx (ровность)':
            self.generate_docx_smooth()
        elif self.comboBox.currentText() == 'Сгенерировать json':
            self.generate_json()
        elif self.comboBox.currentText() == 'Сгенерировать docx (состояние участков в баллах)':
            self.generate_quality_report()
        elif self.comboBox.currentText() == 'Сгенерировать docx (соответствие состояния)':
            self.generate_docx_conformity()
        elif self.comboBox.currentText() == 'Сгенерировать карты (*.png)':
            self.generate_png()
        elif self.comboBox.currentText() == 'Сгенерировать docx (шелехов)':
            self.generate_docx_shelehov()

    @QtCore.pyqtSlot(str, int)
    def onLogged(self, message, level):
        if level == LogModel.ERROR:
            self.progressMain.setValue(self.progressMain.value() + 1)
            if self.progressMain.value() == self.progressMain.maximum():
                self.lblLoading.setVisible(False)
                self.btnGenerate.setDisabled(False)

        self.txtLog.append(message)

    @QtCore.pyqtSlot(object)
    def onReportFinished(self, report):
        self.progressMain.setValue(self.progressMain.value() + 1)
        if self.progressMain.value() == self.progressMain.maximum():
            self.lblLoading.setVisible(False)
            self.btnGenerate.setDisabled(False)
        if report and hasattr(report, 'road'):
            self.txtLog.append("\"{}\" готова".format(report.road.Name))
        else:
            self.txtLog.append("Отчет готов")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
