import sys, re
from os.path import join as p_join
from os.path import dirname, basename
from os import rename
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMainWindow
from PyQt5.QtCore import pyqtSlot, QEvent
from types import MethodType

class drop_handle:
    def dragEnterEvent(self, event):
        drop_handle.mime = event.mimeData()
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            for url in event.mimeData().urls():
                print(url.toLocalFile())
                self.addItem(url.toLocalFile())
        else:
            event.ignore()
        print('drop')

class main_window(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(
            p_join(dirname(__file__), 'main.ui'), baseinstance = self)

        self.vl = self.ui.VList
        self.sl = self.ui.SList

        self.vl.dragEnterEvent = MethodType(drop_handle.dragEnterEvent, self.vl)
        self.sl.dragEnterEvent = MethodType(drop_handle.dragEnterEvent, self.sl)

        self.vl.dragMoveEvent = MethodType(drop_handle.dragMoveEvent, self.vl)
        self.sl.dragMoveEvent = MethodType(drop_handle.dragMoveEvent, self.sl)

        self.vl.dropEvent = MethodType(drop_handle.dropEvent, self.vl)
        self.sl.dropEvent = MethodType(drop_handle.dropEvent, self.sl)
        
        self.ui.show()

    @pyqtSlot()
    def open_videos(self):
        files = QFileDialog.getOpenFileNames()[0]
        for i in files:
            self.vl.addItem(i)

    @pyqtSlot()
    def open_subtitles(self):
        files = QFileDialog.getOpenFileNames()[0]
        for i in files:
            self.sl.addItem(i)

    @pyqtSlot()
    def v_remove(self):
        li_view = self.vl
        for item in li_view.selectedItems():
            li_view.takeItem(li_view.row(item))
            
    @pyqtSlot()
    def s_remove(self):
        li_view = self.sl
        for item in li_view.selectedItems():
            li_view.takeItem(li_view.row(item))

    @pyqtSlot()
    def v_up(self):
        li_view = self.vl
        for item in li_view.selectedItems():
            if item:
                row = li_view.row(item)
                li_view.insertItem(row-1,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def s_up(self):
        li_view = self.sl
        for item in li_view.selectedItems():
            if item:
                row = li_view.row(item)
                li_view.insertItem(row-1,
                                   li_view.takeItem(row))
                

    @pyqtSlot()
    def v_down(self):
        li_view = self.vl
        for item in reversed(li_view.selectedItems()):
            if item:
                row = li_view.row(item)
                li_view.insertItem(row+1,
                                   li_view.takeItem(row))
                
    @pyqtSlot()
    def s_down(self):
        li_view = self.sl
        for item in reversed(li_view.selectedItems()):
            if item:
                row = li_view.row(item)
                li_view.insertItem(row+1,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def v_top(self):
        li_view = self.vl
        for item in reversed(li_view.selectedItems()):
            if item:
                row = li_view.row(item)
                li_view.insertItem(0,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def v_bottom(self):
        li_view = self.vl
        for item in li_view.selectedItems():
            if item:
                row = li_view.row(item)
                li_view.insertItem(li_view.count()-1,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def s_top(self):
        li_view = self.sl
        for item in reversed(li_view.selectedItems()):
            if item:
                row = li_view.row(item)
                li_view.insertItem(0,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def s_bottom(self):
        li_view = self.sl
        for item in li_view.selectedItems():
            if item:
                row = li_view.row(item)
                li_view.insertItem(li_view.count()-1,
                                   li_view.takeItem(row))

    @pyqtSlot()
    def apply(self):
        ext_pattern = re.compile(r'\.[^\.]*$')
        for vid_number in range(self.vl.count()):
            vid_name = self.vl.takeItem(0).text()
            sub_name = self.sl.takeItem(0).text()

            vid_base = basename(vid_name)
            sub_base = basename(sub_name)

            v_res = ext_pattern.search(vid_base)
            s_res = ext_pattern.search(sub_base)
            sub_new_name = (
                p_join(
                    dirname(sub_name),
                    vid_base[:v_res.start()] +
                    sub_base[s_res.start():]
                    )
                )
            rename(sub_name, sub_new_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = main_window()
    sys.exit(app.exec())
