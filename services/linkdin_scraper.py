'''
This file is the backend of the program and handles the searching functions through selenium.
'''

import pickle
from itertools import product
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from app import main

class Driver:
    '''
    The driver class that customize the driver needed for search.
    '''
    def __init__(self, headless):
        self.headless = headless

    def init_driver(self):
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        return webdriver.Firefox(service=Service(), options=options)
    
    def init_wait(self, driver):
        return WebDriverWait(driver, 10)


class Search:
    '''
    The main search class that creates search objects with filtering stuff, job title, and country to search through the jobs.
    '''
    def __init__(self, scope, headless_driver, wait, guisignals):
        self.scope = scope
        self.headless_driver = headless_driver
        self.wait = wait
        self.signals = guisignals
        self.__domain = 'https://www.linkedin.com'
        self.__login_url = 'https://www.linkedin.com/login'
        self.__job_url = 'https://www.linkedin.com/jobs/search/?currentJobId=4239957113&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'

    def search_combinations(self):
        # creates queries of search combinations from the user selected titles and skills for better search
        if not self.scope['title']:
            self.scope['title'].append('')
        if not self.scope['skill']:
            self.scope['skill'].append('')

        combinations = list(product(self.scope['title'], self.scope['skill']))
        queries = [f'{title} {skill}' for title, skill in combinations]
        search_title = ' '
        for query in queries:
            search_title += f'{query} '
        
        return search_title
        
    def __login(self):
        # the login process if the user cookies hasn't been saved yet
        no_headless_Driver = Driver(False)
        no_headless_driver = no_headless_Driver.init_driver()
        no_headless_driver.get(self.__login_url)

        while True:
            current_url = no_headless_driver.current_url
            if 'signup' in current_url:
                # for sign up
                no_headless_driver.close()
                self.signals.error.emit("You can't Sign-Up from this app,\nplease create an account and come back later.")
                time.sleep(5)
                self.signals.quiting.emit()
            elif ('login' not in current_url) and ('checkpoint' not in current_url):
                break
            time.sleep(1)

        main.save_user_pickle(no_headless_driver.get_cookies(), "cookies.pkl")
        no_headless_driver.close()
        self.signals.error.emit('Please wait for search...')

    def __go_to_job_url(self):
        # running the search url
        try:
            self.headless_driver.get(self.__domain)
        except:
            self.signals.error.emit("No internet connection. pleas try again later")
            time.sleep(5)
            self.signals.quiting.emit()
        self.headless_driver.delete_all_cookies()

        try:
            cookies = main.load_user_pickle("cookies.pkl", default=None)
            for cookie in cookies:
                self.headless_driver.add_cookie(cookie)

            self.headless_driver.get(self.__job_url)

            try:
                self.headless_driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div/div/div[2]/button')
                self.signals.error.emit("You have to log-in into your account. Redirecting into log-in page.")
                self.__login()
                self.__go_to_job_url()
            except:
                self.signals.error.emit('Something went wrong!')
        except:
            self.signals.error.emit("You have to log-in into your account. Redirecting into log-in page.")
            self.__login()
            self.__go_to_job_url()

    def search_filter(self, sort: str, date: str, veri: bool, easy: bool, under: bool, scope: dict):
        # adding filters
        filter_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.search-reusables__all-filters-pill-button")))
        filter_button.click()

        self.__load_filter_bar()
        self.__sort_by(sort)
        self.__date_post(date)
        self.__check_boxes(veri, easy, under)
        self.__second_scope(scope)

        show_button = self.headless_driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Apply current filters')]")[0]
        show_button.click()

    def __load_filter_bar(self):
        # loading the filter elements by scrolling through the filter bar
        time.sleep(3)
        self.parent = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog' and contains(@class, 'artdeco-modal')]")))
        self.__scroller = self.parent.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-modal__content')]")
        
        for i in range(5):
            self.headless_driver.execute_script("arguments[0].scrollTop += 300", self.__scroller)
            time.sleep(1.5)

    def __load_filters(self,country):
        self.search_button = self.headless_driver.find_element(By.XPATH, "//button[text()='Search']")
        self.__country(country)
        self.search_button.click()

    def __sort_by(self, status):
        if status == 'Most relevant':
            id = 'advanced-filter-sortBy-R'
        elif status == 'Most recent':
            id = 'advanced-filter-sortBy-DD'

        try:
            button = self.headless_driver.find_element(By.CSS_SELECTOR, f"label[for='{id}']")
            self.headless_driver.execute_script("arguments[0].click();", button)
        except:
            pass

    def __date_post(self, status):
        if status == 'Any time':
            id = 'advanced-filter-timePostedRange-'
        elif status == 'Past month':
            id = 'advanced-filter-timePostedRange-r2592000'
        elif status == 'Past week':
            id = 'advanced-filter-timePostedRange-r604800'
        elif status == 'Past 24 hours':
            id = 'advanced-filter-timePostedRange-r86400'
        
        try:
            button = self.headless_driver.find_element(By.CSS_SELECTOR, f"label[for='{id}']")
            self.headless_driver.execute_script("arguments[0].click();", button)
        except:
            pass

    def __check_boxes(self, veri, easy, under):
        h3s = self.headless_driver.find_elements(By.XPATH, '//h3')
        for h3 in h3s:
            if h3.text == 'Under 10 applicants' and under == True:
                key = self.headless_driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.headless_driver.execute_script("arguments[0].click();", key)

            elif h3.text == 'Has verifications' and veri == True:
                key = self.headless_driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.headless_driver.execute_script("arguments[0].click();", key)

            elif h3.text == 'Easy Apply' and easy == True:
                key = self.headless_driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.headless_driver.execute_script("arguments[0].click();", key)

    def __second_scope(self, scope):
        h3s = self.headless_driver.find_elements(By.XPATH, '//h3')
        for h3 in h3s:
            if h3.text == 'Experience level':
                try:
                    items = self.headless_driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                    for item in items:
                        label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                        if label in scope[h3.text]:
                            self.headless_driver.execute_script("arguments[0].click();", item)
                except:
                    pass

            elif h3.text == 'Job type':
                try:
                    items = self.headless_driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                    for item in items:
                        label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                        if label in scope[h3.text]:
                            self.headless_driver.execute_script("arguments[0].click();", item)
                except:
                    pass

            elif h3.text == 'Remote':
                try:
                    items = self.headless_driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                    for item in items:
                        label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                        if label in scope[h3.text]:
                            self.headless_driver.execute_script("arguments[0].click();", item)
                except:
                    pass

    def __country(self, country):
        country_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="City, state, or zip code"]')))
        country_field.clear()
        country_field.send_keys(country)

    def search(self, queries, filtering: bool, sort=None, date=None, veri=None, easy=None, under=None, scope=None, country=None): # 514 - 524
        # main search function
        self.__go_to_job_url()
        self.search_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')))
        self.search_button = self.headless_driver.find_element(By.XPATH, "//button[text()='Search']")
        self.signals.error.emit('')
        
        self.__load_filters(country=country)
        
        if filtering == True:
            self.signals.error.emit('Adding filters...')
            self.search_filter(sort=sort, date=date, veri=veri, easy=easy, under=under, scope=scope)
            
        
        self.search_field.clear()
        self.search_field.send_keys(queries)
        self.search_button.click()
        self.signals.error.emit('Searching through the jobs...')
        
    

class Extractor:
    '''
    The class for saving the jobs that hab been found in python dictionary and then saving it in a csv file
    '''
    def __init__(self, wait, driver, guisignals):
        self.wait = wait
        self.driver = driver
        self.parent = driver.find_element(By.CSS_SELECTOR, "div.scaffold-layout__list")
        self.__scroller = self.parent.find_element(By.XPATH, "./div[not(self::header)]")
        self.signals = guisignals
        self.global_num = 0
        self.global_page_num = 0
        self.current_page_num = 0

    def __load_jobs(self):
        time.sleep(3)
        last_height = 0
        retries = 0
        while retries < 3:
            self.driver.execute_script("arguments[0].scrollTop += 300", self.__scroller)
            time.sleep(1.5)
            jobs = self.driver.find_elements(By.CLASS_NAME, "job-card-container")

            if len(jobs) >= 25:
                break
            if len(jobs) == last_height:
                retries += 1
            else:
                retries = 0
                last_height = len(jobs)
    
        return jobs
    
    def extract_jobs(self):
        all_jobs = {
            'Job Title': [],
            'Company': [],
            'Location': [],
            'Link': []
        }
        
        time.sleep(5)
        try:
            num_jobs_field = self.driver.find_element(By.XPATH, "//small[contains(@class,'jobs-search-results-list__text')]")
            num, _ = num_jobs_field.text.split()
            if '+' in num:
                self.signals.error.emit("too many jobs, please try again.")
                return None
            
            else:
                try:
                    num_page = (int(num) // 25) + ((int(num) % 25) != 0)
                    self.global_num = int(num)
                    self.global_page_num = num_page
                    self.signals.update.emit(self.global_num, self.global_page_num, self.current_page_num)
                except:
                    num_page = (int(eval(num)[0]*1000+eval(num)[1]) // 25) + ((int(eval(num)[0]*1000+eval(num)[1]) % 25) != 0)
                    self.global_num = eval(num)[0] * 1000 + eval(num)[1]
                    self.global_page_num = num_page

                for i in range(num_page):
                    self.current_page_num = i + 1
                    self.signals.update.emit(self.global_num, self.global_page_num, self.current_page_num)
                    jobs = self.__load_jobs()

                    for job in jobs:
                        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                        all_jobs['Job Title'].append((job.text).split('\n')[0])
                        all_jobs['Company'].append((job.text).split('\n')[2])
                        all_jobs['Location'].append((job.text).split('\n')[3])
                        all_jobs['Link'].append(link)

                    self.driver.execute_script("arguments[0].scrollTop += 300", self.__scroller)
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.jobs-search-pagination__button--next')
                        next_button.click()
                    except:
                        pass

                return all_jobs
            
        except:
            self.global_num = 0
            self.global_page_num = 0
            self.signals.update.emit(self.global_num, self.global_page_num, self.current_page_num)
        
        return None


