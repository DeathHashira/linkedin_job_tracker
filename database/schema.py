'''
This files creates table (if not created) for the user to save the data
'''

import sqlite3

def run():
    conn = sqlite3.connect('linkedin.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
        search_id TEXT NOT NULL,
        search_title TEXT,
        search_date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
    search_id TEXT NOT NULL,
    job_title TEXT,
    job_company TEXT,
    job_location TEXT,
    job_link TEXT
    )
    ''')

    conn.commit()
    conn.close()