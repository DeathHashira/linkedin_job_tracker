from ui import login_automation, job_extraction
from app.config import time
from ui.ui_driver import driver
from app.config import *
from services import linkdin_scraper

job_extraction.search()
time.sleep(3)
linkdin_scraper.export_jobs()
