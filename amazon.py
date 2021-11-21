import csv
import sys

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def get_perc_from_row(row):
    return row.text.split()[2]


def get_page_ranks(driver):
    curr_ranks = []
    elements = driver.find_elements_by_css_selector("a.a-link-normal > span.a-size-base:only-child:not(.a-color-base)")
    review_urls = []
    try:
        review_urls += list(filter(lambda x: "#customerReviews" in x,
                                   map(lambda x: x.find_element_by_xpath('..').get_attribute("href"), elements)))
    except StaleElementReferenceException:
        return get_page_ranks(driver)

    for review_url in review_urls:
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(review_url)

        name = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("productTitle")).text.replace(',', '')
        total = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector("[data-hook=total-review-count]")).text.split()[0].replace(',', '')
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name("a-histogram-row"))
        rows = driver.find_elements_by_class_name("a-histogram-row")

        star5 = list(filter(lambda x: "5 star" in x.text, rows))[0]
        star4 = list(filter(lambda x: "4 star" in x.text, rows))[0]
        star3 = list(filter(lambda x: "3 star" in x.text, rows))[0]
        star2 = list(filter(lambda x: "2 star" in x.text, rows))[0]
        star1 = list(filter(lambda x: "1 star" in x.text, rows))[0]

        curr_ranks.append([name, get_perc_from_row(star5), get_perc_from_row(star4), get_perc_from_row(star3), get_perc_from_row(star2), get_perc_from_row(star1), total])
        print(','.join(curr_ranks[len(curr_ranks) - 1]))

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
        next = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector(".a-last > a"))

        while next and next.get_attribute("href") is not None:
            driver.get(next.get_attribute("href"))
            ranks += get_page_ranks(driver)
            try:
                next = driver.find_element_by_css_selector(".a-last > a")
            except NoSuchElementException:
                break

        driver.close()

    finally:
        header = ['name', 'excellent', 'very_good', 'average', 'poor', 'terrible']

        with open('rankings.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            # writer.writerow(header)

            # write multiple rows
            writer.writerows(ranks)
