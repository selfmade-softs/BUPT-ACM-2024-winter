from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from io import StringIO

def is_exist(by, selector, driver):
    try:
        driver.find_element(by, selector)
    except NoSuchElementException:
        return False
    return True

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
        contests = list(map(lambda contest: {
            'name': contest.text,
            'link': contest.get_attribute('href'),
        }, contests))

        return contests

def get_rank(driver, url):
    driver.switch_to.new_window('tab')
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn-setting'))
        )
    finally:
        setting_button = driver.find_element(By.ID, 'btn-setting')
        setting_button.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'setting-check-all'))
            )
        finally: 
            prev_contests_select = driver.find_element(By.ID, 'setting-check-all')
            if is_exist(By.CSS_SELECTOR, '#contest-setting-table tbody input', driver) and \
                not prev_contests_select.is_selected():
                prev_contests_select.click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#contest-rank-table tbody'))
                )
            finally:
                elem = driver.find_element(By.ID, 'contest-rank-table')
                html = elem.get_attribute('outerHTML')

                return pd.read_html(StringIO(html))[0]
