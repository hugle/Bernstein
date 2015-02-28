import sys

from PyQt5.Qt import *

from GUI.QtUI import Form

app = QApplication(sys.argv)

screen = Form()

screen.show()
sys.exit(app.exec_())
