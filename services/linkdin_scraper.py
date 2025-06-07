import pandas as pd
from itertools import product
import time, json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

class Driver:
    def init_driver(self):
        return webdriver.Firefox(service=Service(), options=Options())
    
    def init_wait(self, driver):
        return WebDriverWait(driver, 10)

class Search:
    def __init__(self, scope, driver, wait):
        self.scope = scope
        self.driver = driver
        self.wait = wait
        self.__domain = 'https://www.linkedin.com'
        self.__login_url = 'https://www.linkedin.com/login'
        self.__job_url = 'https://www.linkedin.com/jobs/search/?currentJobId=4239957113&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    
    def search_combinations(self):
        if not self.scope['title']:
            self.scope['title'].append('')
        if not self.scope['skill']:
            self.scope['skill'].append('')

        combinations = list(product(self.scope['title'], self.scope['skill']))
        queries = [f'{title} {skill}' for title, skill in combinations]
        
        return queries
        
    def __login(self):
        self.driver.get(self.__login_url)

        while True:
            current_url = self.driver.current_url
            if ('login' not in current_url) and ('checkpoint' not in current_url):
                break
            time.sleep(1)

        site_cookies = self.driver.get_cookies()
        with open("linkedin_cookies.json", "w") as file:
            json.dump(site_cookies, file)

    def __go_to_job_url(self):
        self.driver.get(self.__domain)
        self.driver.delete_all_cookies()

        try:
            with open("linkedin_cookies.json", "r") as file:
                cookies = json.load(file)
        
            for cookie in cookies:
                cookie.pop('sameSite', None)
                self.driver.add_cookie(cookie)

            self.driver.get(self.__job_url)

            try:
                self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div/div/div[2]/button')
                self.__login()
                self.__go_to_job_url()
            except:
                pass
        except:
            self.__login()
            self.__go_to_job_url()

    def search_filter(self, sort: str, date: str, veri: bool, easy: bool, under: bool, scope: dict, country):
        filter_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.search-reusables__all-filters-pill-button")))
        filter_button.click()

        self.__load_filter()
        self.__sort_by(sort)
        self.__date_post(date)
        self.__check_boxes(veri, easy, under)
        self.__second_scope(scope)
        self.__country(country)

    def __load_filter(self):
        self.parent = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog' and contains(@class, 'artdeco-modal')]")))
        self.__scroller = self.parent.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-modal__content')]")

        time.sleep(3)
        for i in range(5):
            self.driver.execute_script("arguments[0].scrollTop += 300", self.__scroller)
            time.sleep(1.5)


    def __sort_by(self, status):
        if status == 'Most relevant':
            id = 'advanced-filter-sortBy-R'
        elif status == 'Most recent':
            id = 'advanced-filter-sortBy-DD'

        button = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{id}']")
        self.driver.execute_script("arguments[0].click();", button)

    def __date_post(self, status):
        if status == 'Any time':
            id = 'advanced-filter-timePostedRange-'
        elif status == 'Past month':
            id = 'advanced-filter-timePostedRange-r2592000'
        elif status == 'Past week':
            id = 'advanced-filter-timePostedRange-r604800'
        elif status == 'Past 24 hours':
            id = 'advanced-filter-timePostedRange-r86400'
        
        button = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{id}']")
        self.driver.execute_script("arguments[0].click();", button)

    def __check_boxes(self, veri, easy, under):
        h3s = self.driver.find_elements(By.XPATH, '//h3')
        for h3 in h3s:
            print(h3.text)
            if h3.text == 'Under 10 applicants' and under == True:
                key = self.driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.driver.execute_script("arguments[0].click();", key)

            elif h3.text == 'Has verifications' and veri == True:
                key = self.driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.driver.execute_script("arguments[0].click();", key)

            elif h3.text == 'Easy Apply' and easy == True:
                key = self.driver.find_element(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//div[starts-with(@class, 'artdeco-toggle')]")
                self.driver.execute_script("arguments[0].click();", key)

    def __second_scope(self, scope):
        h3s = self.driver.find_elements(By.XPATH, '//h3')
        for h3 in h3s:
            if h3.text == 'Experience level':
                items = self.driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                for item in items:
                    label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                    if label in scope[h3.text]:
                        self.driver.execute_script("arguments[0].click();", item)


            elif h3.text == 'Job type':
                items = self.driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                for item in items:
                    label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                    if label in scope[h3.text]:
                        self.driver.execute_script("arguments[0].click();", item)


            elif h3.text == 'Remote':
                items = self.driver.find_elements(By.XPATH, f"//h3[normalize-space()='{h3.text}']/ancestor::fieldset//label")

                for item in items:
                    label = item.find_element(By.CSS_SELECTOR, "label span[aria-hidden='true']").text.strip()

                    if label in scope[h3.text]:
                        self.driver.execute_script("arguments[0].click();", item)


    def __country(self, country):
        country_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="City, state, or zip code"]')))
        country_field.clear()
        country_field.send_keys(country)



    def search(self, queries, filtering: bool):
        self.__go_to_job_url()
        self.search_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')))
        self.search_button = self.driver.find_element(By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/button[1]')

        myscope = {
            'Experience level':['Entry level'],
            'Job type':['Full-time', 'Temporary'],
            'Remote':['Remote']
        }

        if filtering == True:
            self.search_filter('Most recent', 'Past month', True, True, True, myscope, 'Sweden')
        
        self.search_field.clear()
        self.search_field.send_keys(queries)
        self.search_button.click()
        
    

class Extractor:
    def __init__(self, wait, driver):
        self.wait = wait
        self.driver = driver
        self.parent = driver.find_element(By.CSS_SELECTOR, "div.scaffold-layout__list")
        self.__scroller = self.parent.find_element(By.XPATH, "./div[not(self::header)]")

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
            num_jobs_field = self.driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list__subtitle')
            num, _ = num_jobs_field.text.split()
            try:
                num_page = (int(num) // 25) + ((int(num) % 25) != 0)
            except:
                num_page = (int(eval(num)[0]*1000+eval(num)[1]) // 25) + ((int(eval(num)[0]*1000+eval(num)[1]) % 25) != 0)

            for _ in range(num_page):
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
        except:
            return None

        return all_jobs

    def export_jobs(self, jobs_dict):
        df = pd.DataFrame(jobs_dict)
        df.to_csv('job_list.csv', index=False, mode='w')

