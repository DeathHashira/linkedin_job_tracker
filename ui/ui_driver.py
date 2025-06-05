from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Firefox(service=Service(), options=Options())
wait = WebDriverWait(driver, 10)