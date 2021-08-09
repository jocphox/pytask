import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sub_setting import dvset
import sub_setting as settings
from ui_control import Ui_MainWindow
from ui_data_view import MenuTW, TWstat
from core_data import DB
from sub_log import dvlog
# Entropy must increase.


class CoreView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # 调用父对象的设置方法，这才将所有的东西给传过来了
        self.setupUi(self)
        # 调用自身额外的一些操作，在QtDesigner中无法实现的操作在此处实现
        #翻译
        self.trans=QTranslator()
        self.today2=QDate.currentDate()
        self.day = (datetime.today()).strftime('%Y-%m-%d %A')
        self.dart_label.setText("pyTask " + self.day)
        self.tw = MenuTW(self.splitter_3)
        self.tw.day = self.day
        self.db = self.tw.db
        # print(self.surf_with_drawing)
        self.acc = settings.account_list
        self.src = settings.source_list
        # log('主界面完成加载。')
        self.setup_UI()

    def setup_UI(self):
        self.cb_language.addItems(['English', "中文"])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.tw.setSizePolicy(sizePolicy)
        self.cb_src.addItems([""] + settings.source_list)
        self.cb_acc.addItems([""] + settings.account_list)
        self.btn_getdata.clicked.connect(self.load_data_analyser)
        self.btn_up.clicked.connect(self.dayup)
        self.btn_down.clicked.connect(self.daydown)
        self.btn_show_ini.clicked.connect(self.showini)
        self.btn_run.clicked.connect(self.showstat) # 花了时间
        self.cb_src.currentIndexChanged.connect(self.showbysource)
        self.cb_acc.currentIndexChanged.connect(self.showbyaccount)
        # self.tw.itemSelectionChanged.connect(self.tw2tb) # 花了时间
        # log("首次加载成功。")
        pass

    def qdatediff(self, qdt1, qdt2):
        return (qdt1.toPyDate()-qdt2.toPyDate()).days

    def showbysourcesource(self):
        self.src = settings.source_list[self.cb_src.currentIndex()-1] if self.cb_src.currentIndex() > 0 else ""
        self.tw.showbysource(self.src)



    def showstat(self):
        self.st = TWstat(self.tw.db,self.tw.day)
        self.st.move(self.tw.pos().x()+self.tw.width(),self.tw.pos().y())
        self.st.resize(450,400)
        self.st.show()

    def autoupdateaccount(self):
        self.db.update_account_auto()

    def d2s(self, qd):
        return qd.toString('YYYY-MM-DD')

    def loadview(self,src):
        viewdata=[]
        viewdata = viewdata + self.db.find(source=src, acc="")
        title = ['id','时间', '日期', '项目', '来源', '主题/标题/文件名', '时长', '信息', '信息2', '备注']
        obj=[self.tv_web,self.tv_local, self.tv_mail,self.tv_mail,self.tv_mail]
        sourcelist=['chrome','local','outbox','calendar','inbox']
        ind= sourcelist.index(src)
        self.loaddata(obj[ind],[x for x in viewdata],title)
        self.tw.setColumnWidth(0,0)

    def loadtask(self):
        self.loadview('outlook')

    def logout(self):
        with open('log.txt','r') as f:
            log = f.read()
        self.msg = QtWidgets.QTextBrowser()
        self.msg.resize(450,self.height())
        self.msg.move(self.pos().x() + self.width(),self.pos().y())
        self.msg.setText(log)
        self.msg.show()

    def loaddata(self,tv,data,title):
        tv.model = QStandardItemModel(len(data), len(title))
        tv.model.setHorizontalHeaderLabels(title) if title else ""
        tv.setColumnWidth(3,200)
        for i in range(len(data)):
            for j in range(len(title)):
                item=QStandardItem(str(data[i][j]))
                tv.model.setItem(i,j,item)
        tv.setModel(tv.model)

    def load_data_analyser(self):
        try:
            if self.tw.loaddata(self.src, self.acc) == 0:
                self.tw.refresh()
                self.tw.loaddata(self.src, self.acc)
            self.load_pic_analyser() if self.surf_with_drawing == 'yes' else 0
        except:

            pass

    def dayup(self):
        pass

    def daydown(self):
        pass

    def runfinal(self):
        pass

    def clicktoimage(self):
        pass

    def showinfo(self,info,pos):
        pass

    def showini(self):
        pass

     # 选择语种的时候
    # def comboBoxChange(self):
    #     self._trigger_english() if str(self.comboBox.currentText()) == "English" else self._trigger_zh_cn()

    def _trigger_english(self):
        #print("[MainWindow] Change to English")
        self.trans.load("en")
        _app = QCoreApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)
        # 重新翻译界面
        self.retranslateUi(self)

    def _trigger_zh_cn(self):
        #print("[MainWindow] Change to zh_CN")
        self.trans.load("zh_cn")
        _app = QCoreApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    showWin = CoreView()
    showWin.show()
    sys.exit(app.exec_())