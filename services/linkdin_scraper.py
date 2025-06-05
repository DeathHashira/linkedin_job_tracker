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
    def __init__(self, filter, keyword, scope, driver, wait):
        self.scope = scope
        self.filter = filter
        self.keyword = keyword
        self.domain = 'https://www.linkedin.com'
        self.login_url = 'https://www.linkedin.com/login'
        self.driver = driver
        self.wait = wait
        self.job_url = 'https://www.linkedin.com/jobs/search/?currentJobId=4239957113&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    
    def search_combinations(self):
        if not self.scope['title']:
            self.scope['title'].append('')
        if not self.scope['skill']:
            self.scope['skill'].append('')
        if not self.scope['company']:
            self.scope['company'].append('')

        combinations = list(product(self.scope['title'], self.scope['skill'], self.scope['company']))
        queries = [f'{title} {skill} {company}' for title, skill, company in combinations]
        if self.filter == True:
            return [query for query in queries if self.keyword in query]
        else:
            return queries
        
    def login(self):
        self.driver.get(self.login_url)

        while True:
            current_url = self.driver.current_url
            if ('login' not in current_url) and ('checkpoint' not in current_url):
                break
            time.sleep(1)

        site_cookies = self.driver.get_cookies()
        with open("linkedin_cookies.json", "w") as file:
            json.dump(site_cookies, file)

    def go_to_job_url(self):
        self.driver.get(self.domain)
        self.driver.delete_all_cookies()

        try:
            with open("linkedin_cookies.json", "r") as file:
                cookies = json.load(file)
        
            for cookie in cookies:
                cookie.pop('sameSite', None)
                self.driver.add_cookie(cookie)

            self.driver.get(self.job_url)

            try:
                self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div/div/div[2]/button')
                self.login()
                self.go_to_job_url()
            except:
                pass
        except:
            self.login()
            self.go_to_job_url()

    def search(self, queries):
        self.go_to_job_url()
        self.search_field = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')
        self.search_button = self.driver.find_element(By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/button[1]')

        self.search_field.clear()
        self.search_field.send_keys(queries)
        self.search_button.click()
    

class Extractor:
    def __init__(self, wait, driver):
        self.wait = wait
        self.driver = driver
        self.scroller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.KCUaezSbBpEYdPJAHVlUbHMAyBsqqRKAb')))

    def load_jobs(self):
        time.sleep(3)
        last_height = 0
        retries = 0
        while retries < 3:
            self.driver.execute_script("arguments[0].scrollTop += 300", self.scroller)
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
        num_jobs_field = self.driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list__subtitle')
        num, _ = num_jobs_field.text.split()
        try:
            num_page = (int(num) // 25) + ((int(num) % 25) != 0)
        except:
            num_page = (int(eval(num)[0]*1000+eval(num)[1]) // 25) + ((int(eval(num)[0]*1000+eval(num)[1]) % 25) != 0)

        for _ in range(num_page):
            jobs = self.load_jobs()

            for job in jobs:
                link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                all_jobs['Job Title'].append((job.text).split('\n')[0])
                all_jobs['Company'].append((job.text).split('\n')[2])
                all_jobs['Location'].append((job.text).split('\n')[3])
                all_jobs['Link'].append(link)

            self.driver.execute_script("arguments[0].scrollTop += 300", self.scroller)
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.jobs-search-pagination__button--next')
                next_button.click()
            except:
                pass

        return all_jobs

    def export_jobs(self, jobs_dict):
        df = pd.DataFrame(jobs_dict)
        df.to_csv('job_list.csv', index=False, mode='w')

