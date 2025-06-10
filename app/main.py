import sys
from ui.ui import *
from services.linkdin_scraper import Driver

driver = Driver(True)

def load_stylesheet(file_path):
    with open(file_path, "r") as f:
        return f.read()

app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("theme.qss"))
MyMainWindow = MyWindow(driver=driver)

MyMainWindow.show()
sys.exit(app.exec())