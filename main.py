import undetected_chromedriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import csv
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def realistic_scroll(browser, direction, max_offset=350, min_offset=300, max_sleep=0.5, min_sleep=0.1):
    offset = random.randint(min_offset, max_offset) * direction
    browser.execute_script(f"window.scrollBy(0, {offset});")
    sleep(random.uniform(min_sleep, max_sleep))


def parsing_market_data(browser):
    logger.info('Gathering market data...')
    actions = ActionChains(browser)

    market_data = browser.find_element(By.CSS_SELECTOR, '#main_navbar  #link_2')
    actions.move_to_element(market_data).perform()
    sleep(1)

    pre_open_market = browser.find_element(By.CSS_SELECTOR, '#main_navbar  a[href*="pre-open-market"]')
    actions.move_to_element(pre_open_market).click().perform()
    sleep(5)

    names = [name.text for name in browser.find_elements(By.CSS_SELECTOR, 'tbody td a[target="_blank"]')]
    final_prices = [price.text.replace(',', '') for price in browser.find_elements(By.CSS_SELECTOR, 'tbody .bold.text-right')]

    logger.info('Market data gathered successfully')
    return list(zip(names, final_prices))


def scroll_page(browser, scrolls=10, direction=1):
    logger.info(f'Scrolling page {scrolls} times in direction {direction}...')
    for _ in range(scrolls):
        realistic_scroll(browser, direction)
    logger.info('Scrolling complete')


def main():
    try:
        with undetected_chromedriver.Chrome() as browser:
            url = 'https://www.nseindia.com/'
            browser.get(url=url)

            data = parsing_market_data(browser)

            logger.info('Custom script started...')
            home_page = browser.find_element(By.CSS_SELECTOR, '#main_navbar #link_0')
            actions = ActionChains(browser)
            actions.move_to_element(home_page).click().perform()
            sleep(2)

            scroll_page(browser, scrolls=10)
            scroll_page(browser, scrolls=10, direction=-1)

            nifty_bank = browser.find_element(By.CSS_SELECTOR, '.tabs_boxes #tabList_NIFTYBANK')
            actions.move_to_element(nifty_bank).click().perform()
            sleep(2)

            scroll_page(browser, scrolls=2)

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
                    break
            sleep(2)

            elements_table = browser.find_elements(By.CSS_SELECTOR, 'tbody > tr')
            for elem in elements_table[:len(elements_table) - 28]:
                browser.execute_script('return arguments[0].scrollIntoView(true);', elem)
                sleep(0.15)

            sleep(2)
            logger.info('User script completed successfully')

    except Exception as e:
        logger.error(f'An error occurred: {e}')

    with open('res.csv', 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Price'])
        for i in range(len(data)):
            writer.writerow([data[i][0], data[i][1]])


if __name__ == "__main__":
    main()
