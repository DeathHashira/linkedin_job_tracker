from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

driver = webdriver.Firefox(service=Service(), options=Options())