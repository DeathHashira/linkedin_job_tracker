'''
The main program that connects the backend and frontend together by creating the objects and running the program.
'''

import sys, os, shutil, pickle
from ui.ui import *
from services.linkdin_scraper import Driver
from database import schema
from pathlib import Path

app_name = "Jobolist"

def get_user_data_dir():
    home = Path.home()
    if sys.platform.startswith('win'):
        base = Path(os.getenv("APPDATA", home / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = home / "Library" / "Application Support"
    else:
        base = Path(os.getenv("XDG_DATA_HOME", home / ".local" / "share"))
    
    d = base / app_name
    d.mkdir(parents=True, exist_ok=True)
    return d

def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent
    return base / "resources" / rel

def ensure_user_db():
    user_db = get_user_data_dir() / "linkedin.db"
    if not user_db.exists():
        template = resource_path("default.db")
        if template.exists():
            shutil.copy(template, user_db)
        else:
            user_db.touch()
    return user_db

def get_user_pickle_path(name):
    return get_user_data_dir() / name

def load_user_pickle(name, default=None):
    p = get_user_pickle_path(name)
    if p.exists():
        with open(p, "rb") as f:
            return pickle.load(f)
    return default

def save_user_pickle(obj, name):
    with open(get_user_pickle_path(name), "wb") as f:
        pickle.dump(obj, f)

db_path = ensure_user_db()
if not db_path.exists():
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