from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from time import sleep

from ecs import all_elements_contains_name
from utils import *

firefox_options = FirefoxOptions()
firefox_options.add_argument('--headless')
# http_proxy_server_url = 'localhost:10809'
# firefox_options.add_argument('--proxy-server=' + http_proxy_server_url)
# firefox_options.add_argument('--ignore-certificate-errors')
# firefox_options.add_argument('--ignore-ssl-errors')
# firefox_options.add_argument('user-agent=fake-useragent')

driver = webdriver.Firefox(options=firefox_options)

vjudge_prefix='https://vjudge.net'
contest_prefix='BUPT 2024 Winter Welcome Wagon'
poster_username='Oranger_cc'
# driver.implicitly_wait(10)

contests=get_contests(driver, 
    url=f'{vjudge_prefix}/contest#category=public&running=3&title={contest_prefix}&owner={poster_username}')
print('contest links got')
print(contests)

for contest in contests:
    rank=get_rank(driver, url=f'{contest["link"]}#rank')
    # rank.columns = rank.columns.get_level_values(0)
    rank.to_excel(f'ranks/{contest["name"].split(":")[0]}.xlsx')

print('ranks got')
driver.quit()

