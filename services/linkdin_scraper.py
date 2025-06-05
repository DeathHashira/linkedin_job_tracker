from app.config import *
from ui.ui_driver import driver, wait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def load_jobs():
    time.sleep(3)
    scroller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.EtTYpyMUyhdoALZmjXTSvgbVEJnyQFGRynGadR')))
    
    last_height = 0
    retries = 0
    
    while retries < 3:
        driver.execute_script("arguments[0].scrollTop += 300", scroller)
        time.sleep(1.5)

        jobs = driver.find_elements(By.CLASS_NAME, "job-card-container")

        if len(jobs) >= 25:
            break

        if len(jobs) == last_height:
            retries += 1
        else:
            retries = 0
            last_height = len(jobs)
    
    return jobs
    
def extract_jobs():
    all_jobs = {
        'Job Title': [],
        'Company': [],
        'Location': [],
        'Link': []
    }

    num_jobs_field = driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list__subtitle > span:nth-child(1)')
    num, _ = num_jobs_field.text.split()
    try:
        num_page = (int(num) // 25) + ((int(num) % 25) != 0)
    except:
        num_page = (int(eval(num)[0]*1000+eval(num)[1]) // 25) + ((int(eval(num)[0]*1000+eval(num)[1]) % 25) != 0)

    for i in range(num_page):
        jobs = load_jobs()

        for job in jobs:
            link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
            all_jobs['Job Title'].append((job.text).split('\n')[0])
            all_jobs['Company'].append((job.text).split('\n')[2])
            all_jobs['Location'].append((job.text).split('\n')[3])
            all_jobs['Link'].append(link)

        scroller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.EtTYpyMUyhdoALZmjXTSvgbVEJnyQFGRynGadR')))
        driver.execute_script("arguments[0].scrollTop += 300", scroller)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '#ember285')
            next_button.click()
        except:
            pass

    return all_jobs

def export_jobs():
    df = pd.DataFrame(extract_jobs())
    df.to_csv('job_list.csv', index=False)

