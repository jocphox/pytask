# the output
import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication,QSizePolicy,QMainWindow, QComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sub_setting import dvset
import sub_setting as settings
import random
from ui_control2 import Ui_MainWindow

class CoreView(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # 调用父对象的设置方法，这才将所有的东西给传过来了
        self.setupUi(self)
        # 调用自身额外的一些操作，在QtDesigner中无法实现的操作在此处实现
        #翻译
        self.trans = QTranslator()
        self.today2 = QDate.currentDate()
        self.day = (datetime.today()).strftime('%Y-%m-%d %A')
        self.dart_label.setText("pyTask " + self.day)
        # print(self.surf_with_drawing)
        self.data = self.gendata()
        self.acc = settings.account_list
        self.acc.insert(0,"")
        self.src = settings.source_list
        self.src.insert(0,"")
        self.header = ['data', 'source', 'account','value', 'yn','prop']
        self.lw.setRowCount(len(self.header))
        # log('主界面完成加载。')

        self.build_lw()
        self.load(self.data)
        self.setup_UI()



    def setup_UI(self):
        self.cb_language.addItems(['English', "中文"])
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tw.setSizePolicy(sizePolicy)
        self.btn_run.clicked.connect(self.showstat) # 花了时间
        self.tw.itemSelectionChanged.connect(self.tw2lw) # 花了时间
        self.tw.itemClicked.connect(self.editmode)  # 花了时间
        # self.lw.cellWidget(2, 1).currentIndexChanged.connect(self.refreshview)
        # self.lw.cellWidget(1, 1).currentIndexChanged.connect(self.refreshview)

        # log("首次加载成功。")
        pass

    def refreshview(self):
        source = self.lw.cellWidget(1,1).currentText()
        account = self.lw.cellWidget(2,1).currentText()
        print(source == "",account == "")
        # print(self.find2(source,account))
        self.load(self.find2(source, account))
        pass

    def find2(self, source, account):

        # data =[[self.tw.item(i,j).text() for j in range(self.tw.columnCount())] for i in range(self.tw.rowCount())]
        # print(data)
        data = self.data
        newdata = list(filter(lambda x: (x[self.header.index('source')] == source or source == "") and
                                           (x[self.header.index('account')] == account or account == "")
                                 , data))
        print(newdata)
        return newdata

    def build_cb(self):
        pass

    def build_lw(self):
        items = [[self.header[i], ""] for i in range(self.tw.columnCount())]
        for i in range(self.lw.rowCount()):
            for j in range(self.lw.columnCount()):
                self.lw.setItem(i, j, QTableWidgetItem(str(items[i][j])))
        cb_src = QComboBox()
        cb_acc = QComboBox()
        cb_src.addItems(self.src)
        cb_acc.addItems(self.acc)
        self.lw.setCellWidget(1, 1, cb_src)
        self.lw.setCellWidget(2, 1, cb_acc)



    def tw2lw(self):

        self.lw.clear()
        ind = self.tw.selectionModel().selection().indexes()[0].row()
        items = [[self.header[i], self.tw.item(ind, i).text()] for i in range(self.tw.columnCount())]
        for i in range(self.lw.rowCount()):
            for j in range(self.lw.columnCount()):
                self.lw.setItem(i, j, QTableWidgetItem(str(items[i][j])))


        # items_with_header = list(zip(self.header, items))
        # self.lw.addItems(items)
        pass

    def editmode(self):
        self.cleancellWidget()
        index = self.tw.selectionModel().selection().indexes()[0]
        x, y = (index.row(), index.column())
        if y in [1, 2]:
            cb_src = QComboBox()
            cb_acc = QComboBox()
            cb_src.addItems(self.src)
            cb_acc.addItems(self.acc)
            cb = [cb_src, cb_acc][y-1]
            self.tw.setCellWidget(x, y, cb)
            self.tw.cellWidget(x, y).setCurrentText(self.tw.item(x,y).text())
            self.tw.cellWidget(x,y).currentIndexChanged.connect(lambda:
                self.tw.setItem(x,y,QTableWidgetItem(self.tw.cellWidget(x,y).currentText())))
            self.tw.cellWidget(x, y).currentIndexChanged.connect(self.tw2lw)

    def cleancellWidget(self):
        for i  in range(self.tw.rowCount()):
            for j in range(1,3):
                try:
                    # print(i,j)
                    self.tw.removeCellWidget(i,j)

                except:
                    pass
        pass

    def load(self, data):
        if len(data) == 0 :
            for i in range(self.tw.rowCount()):
                for j in range(self.tw.columnCount()):
                    self.tw.setItem(i, j, QTableWidgetItem(""))
        else:
            self.tw.setColumnCount(len(data[0]))
            self.tw.setRowCount(len(data))
            self.tw.setHorizontalHeaderLabels(self.header)
            for i in range(self.tw.rowCount()):
                for j in range(self.tw.columnCount()):
                    self.tw.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def showstat(self):
        pass

    def gendata(self):

        def listgendata(lst):
            return lst[random.randint(0,len(lst)-1)]

        gendata = lambda i: ['data' + str(i)] + list(map(listgendata,[settings.source_list, settings.account_list, range(1, 10), [1], ['test']]))
        data = list(map(gendata, range(0,10)))
        return data
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = CoreView()
    # print(a.gendata())
    a.show()
    sys.exit(app.exec_())