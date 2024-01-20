from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO

def get_contests(driver, url):
    driver.get(url)
    assert 'Contest' in driver.title
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'contest_entry'))
        )
    finally:
        elem = driver.find_element(By.ID, 'listContest')

        contests = elem.find_elements(By.CLASS_NAME, 'contest_entry')
        return list(map(lambda contest: {
            'name': contest.text,
            'link': contest.get_attribute('href'),
        }, contests))

def get_rank(driver, url):
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#contest-rank-table tbody'))
        )
    finally:
        elem = driver.find_element(By.ID, 'contest-rank-table')
        html = elem.get_attribute('outerHTML')
        return pd.read_html(StringIO(html))[0]
