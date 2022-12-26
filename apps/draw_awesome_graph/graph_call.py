import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QFileSystemModel, QFileDialog

# Key Event
from PySide6.QtCore import Qt

import pyqtgraph as pg
from graphPlotUi import Ui_MainWindow

# 自作のライブラリ
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

        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setNameFilters(['*.py']) # この設定だけだと、非該当の拡張子はグレー表示
        self.model.setNameFilterDisables(False) # 上記フィルターに該当しないファイルは非表示

        view = self.treeView
        view.setModel(self.model)
        view.setRootIndex(self.model.index(path))
        view.setColumnWidth(0,260)
        # doubleClicked ...
        view.clicked.connect(self.setFileName)


        # ハイライト表示
        self.hl = PythonHighlighter(self.codeView.document())

        # ボタン操作
        self.saveButton.clicked.connect(self.saveFile)
        self.plotButton.clicked.connect(self.generate_xy)
        self.clearButton.clicked.connect(self.clear)
        self.fontCssLegend = '<style type="text/css"> p {font-family: Helvetica, HackGen35 Console NFJ; font-size: 15pt; color: "#ffffff"} </style>'
        self.codeView.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.codeView:
            if event.key() == Qt.Key_Tab and self.codeView.hasFocus():
                # Special tab handling
                tc = self.codeView.textCursor()
                tc.insertText("    ")
                return True
            else:
                return False
        return False


    def onTextChange(self):
        """
        textChanged fires when the highlighter is reassigned the same document.
        Prevent this from showing "run edited code" by checking for actual
        content change
        """
        newText = self.codeView.toPlainText()
        if newText != self.oldText:
            self.oldText = newText
            #self.codeEdited() 


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
                self.codeView.setPlainText(text)
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
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","python Files (*.py)", options=options)
        try:
            with open(fileName, 'w', encoding='utf-8') as f:
                f.write(self.codeView.toPlainText()) 
        except FileNotFoundError as e:
            pass



    def clear(self):
        self.codeView.clear()


    def generate_xy(self):
        sampleCode = self.codeView.toPlainText()
        addCode='''
self.draw_graph(x,y,name_of_graph,name_of_xaxis,name_of_yaxis,symbolSize)
'''
        exec(sampleCode+addCode)


    def draw_graph(self,x,y,name_of_graph,name_of_xaxis,name_of_yaxis,symbolSize):
        self.fontCssLegend = '<style type="text/css"> p {font-family: Helvetica, HackGen35 Console NFJ; font-size: 15pt; color: "#ffffff"} </style>'
        styles = {'color':'white',
                        'font-size':'20px',
                        'font-style':'bold',
                        'font-family': 'Helvetica, HackGen35 Console NFJ'
                        }
        import inspect
        def retrieve_name(var):
            callers_local_vars = inspect.currentframe().f_back.f_locals.items()
            return [var_name for var_name, var_val in callers_local_vars if var_val is var]

        setprop = lambda x: (x.setAutoVisible(y=True),
                            x.enableAutoRange(False),
                            x.showAxis('right'),
                            x.showAxis('left'),
                            x.showAxis('top'),
                            x.getAxis('top').setHeight(30),
                            x.getAxis('bottom').setHeight(50),
                            x.getAxis('right').setWidth(50),
                            x.getAxis('left').setWidth(50),
                            x.showGrid(x=True, y=True, alpha = 1),
                            x.setAutoVisible(y=True),
                            #x.setXRange(-1, 1, padding=0.1),
                            #x.setYRange(-1, 1, padding=0.1),
                            x.addLegend(offset=(10,10)),
                            x.setTitle('<font size=\'14\' color=\'#FFFFFF\'>'+ name_of_graph +'</font>'),
                            x.setLabel('left'  , text=name_of_yaxis, units='', **styles),
                            x.setLabel('bottom', text=name_of_xaxis, units='', **styles),
                            #x.setLabel('right'  , text='y', units='', **styles),
                            #x.setLabel('top', text='x', units='', **styles),
                            )
        self.glw.clear()
        p1 = self.glw.addPlot()
        setprop(p1)
        p1.plot(x, y,
                clear=True,
                pen='#0F0',
                alpha=1,
                symbolBrush='#0F0',
                symbolSize=symbolSize,
                #name=self.fontCssLegend + '<p>'+name+'</p>'
                )



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
