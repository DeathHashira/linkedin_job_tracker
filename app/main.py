'''
The main program that connects the backend and frontend together by creating the objects and running the program.
'''

import sys, os
from ui.ui import *
from services.linkdin_scraper import Driver
from database import schema

if not os.path.exists('linkedin.db'):
    schema.run()

driver = Driver(True)

def load_stylesheet(file_path):
    with open(file_path, "r") as f:
        return f.read()

app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("theme.qss"))
MyMainWindow = MyWindow(driver=driver)

MyMainWindow.show()
sys.exit(app.exec())