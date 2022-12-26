import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QFileSystemModel, QFileDialog

from mapPlotUi import Ui_MainWindow

import io
import folium
from folium import plugins

# 自作のライブラリ
from commands.make_tableview_mode import *
from my_modules.syntax_highlighter import *

def _clearall(layout):
    children = []
    for i in range(layout.count()):
        child = layout.itemAt(i).widget()
        if child:
            children.append(child)
    for child in children:
        child.deleteLater()
    else:
        pass

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # pathを引数にて指定
        try:
            path = sys.argv[1]
        except IndexError:
            path = '.'
        self.filepath = []

        self.hl = PythonHighlighter(self.plainTextEdit.document())

        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setNameFilters(['*.fo']) # この設定だけだと、非該当の拡張子はグレー表示
        self.model.setNameFilterDisables(False) # 上記フィルターに該当しないファイルは非表示

        view = self.treeView
        view.setModel(self.model)
        view.setRootIndex(self.model.index(path))
        view.setColumnWidth(0,260)
        # doubleClicked ...
        view.clicked.connect(self.setFileName)


        self.saveButton.clicked.connect(self.saveFile)
        self.plotButton.clicked.connect(self.mapPlot)
        self.clearButton.clicked.connect(self.clear)


    def init_ui(self):
        self.setGeometry(50, 50, 1200, 960) # WQXGA (Wide-QXGA)
        self.fontCssLegend = '<style type="text/css"> p {font-family: Arial;font-size: 16pt; color: "#FFF"} </style>'


    def setFileName(self, index):
        try:
            import os
            indexItem = self.model.index(index.row(), 0, index.parent())#print(indexItem)
            if os.path.isfile(self.model.filePath(indexItem)):
                self.filepath.insert(0,self.model.filePath(indexItem))
                text = open(self.filepath[0], encoding='utf-8').read()
                self.plainTextEdit.setPlainText(text)
                text.close()
                #self.filepath.insert(0,self.model.filePath(indexItem))
                #self.listWData.clear()
                #self.listWData.addItems(df.columns)
                #self.graphPlot()
            else:
                pass
                #QMessageBox.warning(None, "Notice!", "Select File!",QMessageBox.Yes)
        except AttributeError as e:
            pass


    def saveFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","folium Obj Files (*.fo)", options=options)
        try:
            with open(fileName, 'w', encoding='utf-8') as f:
                f.write(self.plainTextEdit.toPlainText()) 
        except FileNotFoundError as e:
            pass



    def clear(self):
        self.plainTextEdit.clear()

    def mapPlot(self):
        #_clearall(self.layout)
        sampleCode = self.plainTextEdit.toPlainText()

        addCode='''
data = io.BytesIO()
m.save(data, close_file=False)
self.widget.setHtml(data.getvalue().decode())
'''

        exec(sampleCode+addCode)


def main():
    #import qdarktheme
    app = QApplication(sys.argv)
    # Apply dark theme to Qt application
    #app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()

if __name__== '__main__':
    main()
