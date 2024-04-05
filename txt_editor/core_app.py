import sys
from PySide6.QtWidgets import QApplication
from display_app import MainDisplay

app = QApplication(sys.argv)
w = MainDisplay(app)
w.show()
app.exec()