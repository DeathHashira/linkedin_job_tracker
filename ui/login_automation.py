import requests, urllib.parse, time, json
from app.config import *
from ui.ui_driver import driver

def request_code():
    prams = {
        'response_type':'code',
        'redirect_uri':redirect_uri,
        'client_id':client_id,
        'scope':scope
    }
    url = 'https://www.linkedin.com/oauth/v2/authorization?' + urllib.parse.urlencode(prams)
    driver.get(url)

    while True:
        current_url = driver.current_url
        if redirect_uri in current_url:
            break
        time.sleep(1)
    
    parsed_url = urllib.parse.urlparse(current_url)
    qprams = urllib.parse.parse_qs(parsed_url.query)
    driver.quit()
    return qprams.get('code')[0]

def access_token():
    code = request_code()
    header = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    prams = {
        'grant_type':'authorization_code',
        'code':code,
        'client_id':client_id,
        'client_secret':client_secret,
        'redirect_uri':redirect_uri
    }
    url = 'https://www.linkedin.com/oauth/v2/accessToken'

    res = requests.post(url=url, headers=header, data=prams)
    return res.json()['access_token']


