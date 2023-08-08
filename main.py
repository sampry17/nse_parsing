import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import csv
import random
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service


def realistic_scroll(browser, direction, max_offset=350, min_offset=300, max_sleep=0.5, min_sleep=0.1):
    offset = random.randint(min_offset, max_offset) * direction
    browser.execute_script(f"window.scrollBy(0, {offset});")
    sleep(random.uniform(min_sleep, max_sleep))


try:
    with undetected_chromedriver.Chrome() as browser:
        url = 'https://www.nseindia.com/'
        browser.get(url=url)
        actions = ActionChains(browser)

        market_data = browser.find_element(By.XPATH, '//div[@id="main_navbar"]//a[@id="link_2"]')
        actions.move_to_element(market_data).perform()
        sleep(1)

        pre_open_market = browser.find_element(By.XPATH, '//*[@id="main_navbar"]/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a')
        actions.move_to_element(pre_open_market).click().perform()
        sleep(5)

        names = [name.text for name in browser.find_elements(By.XPATH, '//tbody//td//a[@target="_blank"]')]
        final_prices = [price.text.replace(',', '') for price in browser.find_elements(By.XPATH, '//tbody//td[@class="bold text-right"]')]

        data = list(zip(names, final_prices))

        home_page = browser.find_element(By.XPATH, '//div[@id="main_navbar"]//a[@id="link_0"]')
        actions.move_to_element(home_page).click().perform()
        sleep(2)

        for i in range(10):
            realistic_scroll(browser, 1)

        for i in range(10):
            realistic_scroll(browser, -1)

        nifty_bank = browser.find_element(By.XPATH, '//nav[@class="tabs_boxes"]//a[@id="tabList_NIFTYBANK"]')
        actions.move_to_element(nifty_bank).click().perform()
        sleep(2)

        for i in range(2):
            realistic_scroll(browser, 1)

        view_all = browser.find_element(By.CSS_SELECTOR, '#tab4_gainers_loosers > .link-wrap > a')
        sleep(2)
        actions.move_to_element(view_all).click().perform()
        sleep(2)

        selector = browser.find_element(By.CSS_SELECTOR, '.selectbox.head_selectbox #liveMrktStockSel')
        actions.move_to_element(selector).click().perform()
        sleep(2)

        for elem in browser.find_elements(By.CSS_SELECTOR, '.selectbox.head_selectbox #liveMrktStockSel [data-nse-translate="symbol"]'):
            browser.execute_script('return arguments[0].scrollIntoView(true);', elem)
            if elem.get_attribute('value') == 'NIFTY ALPHA 50':
                elem.click()
        sleep(2)

        elements_table = browser.find_elements(By.XPATH, '//tbody//td[@class="bold text-right lowHighInd"]/..')
        for elem in elements_table[:len(elements_table) - 18]:
            browser.execute_script('return arguments[0].scrollIntoView(true);', elem)
            sleep(0.15)

        sleep(2)
        actions.reset_actions()

except Exception as e:
    print('error')


with open('res.csv', 'w', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Name', 'Price'])
    for i in range(len(data)):
        writer.writerow([data[i][0], data[i][1]])
