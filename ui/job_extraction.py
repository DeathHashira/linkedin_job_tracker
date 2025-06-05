from app.config import *
from itertools import product
from ui.ui_driver import driver
from ui import login_automation

scope = {
    'title': ['backend', 'data'],
    'skill': ['python', 'node.js'],
    'company': []
}


def search_combinations(scope):
    if not scope['title']:
        scope['title'].append('')
    if not scope['skill']:
        scope['skill'].append('')
    if not scope['company']:
        scope['company'].append('')

    combinations = list(product(scope['title'], scope['skill'], scope['company']))
    queries = [f'{title} {skill} {company}' for title, skill, company in combinations]

    return queries

def filter(keyword):
    queries = search_combinations()
    filtered = [query for query in queries if keyword in query]
    
    return filtered


def go_to_job_url():
    driver.get("https://www.linkedin.com")
    driver.delete_all_cookies()
    try:
        with open("linkedin_cookies.json", "r") as file:
            cookies = json.load(file)
        
        for cookie in cookies:
            cookie.pop('sameSite', None)
            driver.add_cookie(cookie)

        driver.get(job_url)

        try:
            driver.find_element(By.XPATH, '/html/body/div[5]/div/div/section/div/div/div/div[2]/button')
            login_automation.login()
            go_to_job_url()
        except:
            pass
    except:
        login_automation.login()
        go_to_job_url()
        
def search():
    go_to_job_url()
    search_field = driver.find_element(By.XPATH, '//*[@id="jobs-search-box-keyword-id-ember32"]')
    search_button = driver.find_element(By.XPATH, '/html/body/div[6]/header/div/div/div/div[2]/button[1]')

    search_field.clear()
    search_field.send_keys(search_combinations(scope))
    search_button.click()
