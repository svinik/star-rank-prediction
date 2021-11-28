import csv
import sys

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def get_page_ranks(driver):
    curr_ranks = []
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("review_count"))
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review_count")))
    reviews = driver.find_elements_by_class_name("review_count")
    review_urls = []
    try:
        review_urls += list(map(lambda x: x.get_attribute("href"), filter(lambda x: x.text != '0 reviews', reviews)))
    except StaleElementReferenceException:
        return get_page_ranks(driver)

    for review_url in review_urls:

        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(review_url)

        name = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("HEADING")).text.replace(',', '')
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("dQNlC"))
        rankings = driver.find_elements_by_class_name("dQNlC")

        curr_ranks.append([review_url, name, get_rank_text(rankings[0]), get_rank_text(rankings[1]), get_rank_text(rankings[2]),
                      get_rank_text(rankings[3]), get_rank_text(rankings[4])])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return curr_ranks


def get_rank_text(rank):
    splits = rank.text.split()
    num = splits[1] if splits[1] != 'Good' else splits[2]
    return num.replace(',', '')


if __name__ == '__main__':
    url = sys.argv[1]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)

    ranks = []

    try:
        ranks += get_page_ranks(driver)
        next = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("next"))

        while next.get_attribute("href") is not None:
            driver.get(next.get_attribute("href"))
            ranks += get_page_ranks(driver)
            next = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("next"))

        driver.close()

    finally:
        header = ['url', 'name', 'excellent', 'very_good', 'average', 'poor', 'terrible']

        with open('hotel_rankings.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            # writer.writerow(header)

            # write multiple rows
            writer.writerows(ranks)
