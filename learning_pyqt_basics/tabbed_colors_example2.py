import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QColor  # ✅ Correct import

from layout_colorwidget import Color  # Your custom widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print(QColor.colorNames())  # ✅ This now works

        self.setWindowTitle("My App")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)

        for color in QColor.colorNames():  # ✅ Iterate through all named colors
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
