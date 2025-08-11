'''
This file handles the functions for chaging and inserting data into the database
'''

import sqlite3, string, random

def code():
    possibility = string.ascii_letters + string.digits
    verified_code = ''.join(random.choice(possibility) for _ in range(64))
    
    return verified_code


def new_search(name:str, date:str):
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()
    search_code = code()
    cursor.execute('''
        INSERT INTO searches (search_id, search_title, search_date) VALUES (?, ?, ?)
    ''', (search_code, name, date))
    conn.commit()
    conn.close()

    return search_code

def add_job(code:str, job_title:str, job_location:str,
                    job_company:str, job_link:str):
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (job_title, job_company, job_location, job_link, search_id) VALUES (?, ?, ?, ?, ?)
    ''', (job_title, job_company, job_location, job_link, code))
    conn.commit()

def show_searches():
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT search_title, search_date FROM searches
    ''')

    return cursor.fetchall()

def show_jobs(search_title):
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT job_title, job_company, job_location, job_link
        FROM searches
        JOIN jobs ON searches.search_id = jobs.search_id
        WHERE search_title = ?
    ''', (search_title,))

    return cursor.fetchall()

