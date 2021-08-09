import sys
from view_process import CoreView
from PyQt5.QtWidgets import  QApplication





if __name__ == '__main__':

    app = QApplication(sys.argv)
    showWin = CoreView()
    showWin.show()
    sys.exit(app.exec_())