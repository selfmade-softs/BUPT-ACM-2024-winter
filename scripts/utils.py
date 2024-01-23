from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
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

    setting_button = driver.find_element(By.ID, 'btn-setting')
    setting_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'setting-check-all'))
        )
    finally: 
        prev_contests_select = driver.find_element(By.ID, 'setting-check-all')
        if prev_contests_select is not None and not prev_contests_select.is_selected():
            prev_contests_select.click()

        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contest-rank-table tbody'))
            )
        finally:
            elem = driver.find_element(By.ID, 'contest-rank-table')
            html = elem.get_attribute('outerHTML')
            return pd.read_html(StringIO(html))[0]
