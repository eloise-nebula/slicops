import asyncio
import gc
import pprint
import pykern
import queue
import slicops.sliclet
import threading


# from PyQt5.QtWidgets import (
#     QApplication, QPushButton, QMainWindow, QBoxHLayout, QBoxVLayout
# )


# Subclass QMainWindow to customize your application's main window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#     def build_cell(self, ui_layout):
#         pass

#     def build_col(self, ui_layout):
#         pass

#     def build_row(self, ui_layout):
#         pass

#     def handle_start(self, ui_layout):
#         pass

# class _Worker():
#     def __init__(self, window):
#         self.__window = window
#         self._queue = queue()

#     def _destroy(self):
#         pass

#     def run(self):
#         asyncio.run(self._loop())

#     async def _loop(self):
#         while (r := await self._queue.get()):
#             pass    
    

async def main():
    q = None
    i = None
    try:
        q = asyncio.Queue()
        i = slicops.sliclet.instance("yaml_db", q)
        r = await q.get()
        pprint.pprint(r["ui_layout"])
    finally:
        del i
        gc.collect()

# app = QApplication()

# window = MainWindow()
# window.show()

# print(window.children()[0].name)

# app.exec()

asyncio.run(main())
