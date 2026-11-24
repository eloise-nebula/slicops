from pykern.pkdebug import pkdlog
import queue
import slicops.sliclet
import threading
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel, QVBoxLayout,
)


class MainWindow(QMainWindow):
    send_update = pyqtSignal(dict)
    
    def __init__(self, parent=None, sliclet="hello"):
        super().__init__(parent=parent)
        self._thread = QThread()
        self._worker = _Worker(self, sliclet=sliclet)
        self._worker.moveToThread(self._thread)
        self._worker.ctx_update.connect(self.ctx_update)
        self._thread.started.connect(self._worker.run)
        self.send_update.connect(self.field_write)
        self.fields = {}
        main_widget = QWidget()
        self.main_widget = main_widget
        self.setCentralWidget(main_widget)
        self._thread.start()

    @pyqtSlot(dict)
    def ctx_update(self, r):
        self.fields = r.fields
        self.build_row(r.ui_layout, self.main_widget)

    @pyqtSlot(dict)
    def field_write(self, field_values):
        self._worker.queue.put_nowait({"field_values": field_values})

    def build_cell(self, r, parent):
        field = self.fields[r.field]
        if field.ui.widget in ["string", "float", "integer"]:
            parent.addWidget(QLabel(field.value))
        else:
            ValueError(f"Unsupported widget={w}")

    def build_col(self, ui_layout, parent):
        layout = QVBoxLayout()
        for r in ui_layout.cols:
            if r.layout == "rows":
                self.build_row(r, layout)
            elif r.layout == "cell":
                self.build_cell(r, layout)
            else:
                ValueError(f"Unsupported layout={r.layout} for parent=col")

    def build_row(self, ui_layout, parent):
        layout = QHBoxLayout(parent)
        for r in ui_layout.rows:
            if r.layout == "cols":
                self.build_col(r, layout)
            elif r.layout == "cell":
                self.build_cell(r, layout)
            else:
                ValueError(f"Unsupported layout={r.layout} for parent=row")

class _Worker(QObject):
    destroyed = pyqtSignal()
    ctx_update = pyqtSignal(dict)
    
    def __init__(self, window, sliclet="hello", **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.queue = queue.Queue()
        # Make a fake update_q.put_nowait to better integrate w qobject?
        self.sliclet = slicops.sliclet.instance(sliclet, self.queue)

    def run(self):
        while (r := self.queue.get()):
            if "ui_layout" in r:
                self.ctx_update.emit(r)
            if "field_values" in r:
                self.sliclet.ctx_write(r)

    def destroy(self):
        self.destroyed.emit()

