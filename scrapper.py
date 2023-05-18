from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from unittest.mock import Mock
from selenium.webdriver.support import expected_conditions as EC
import csv

class fakeElement:
    text = ''

def collect_from_product_page():
    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1")
    except NoSuchElementException:
        title = fakeElement()
    try:
        brand = driver.find_element(By.CSS_SELECTOR, "p a, p span")
    except NoSuchElementException:
        brand = fakeElement()
    try:
        description = driver.find_element(By.XPATH, "//div[contains(@itemprop, 'description')]")
    except NoSuchElementException:
        description = fakeElement()
    try:
        price = driver.find_element(By.CLASS_NAME, "prix")
    except NoSuchElementException:
        price = fakeElement()
    try:
        img = driver.find_element(By.CLASS_NAME, "media-object")
    except NoSuchElementException:
        img = fakeElement()
    # PRODUCT SELLERS AND PRICE
    try:
        sellers_elements = driver.find_elements(By.XPATH, "//td[@itemprop='seller']")
        sellers = ''

        for i, seller in enumerate(sellers_elements):
            if (i != 0):
                sellers += '\n'
            sellers += seller.text
    except:
        pass
    try:
        sellers_prices_elements = driver.find_elements(By.XPATH, "//span[@itemprop='price']")
        seller_prices = ''

        for i, seller_price in enumerate(sellers_prices_elements):
            if (i != 0):
                seller_prices += '\n'
            seller_prices += seller_price.text + ' €'
    except:
        pass

    print([driver.current_url, title.text, brand.text, description.text, (price.text).replace('Prix moyen : ', ''), img.get_attribute("src"), sellers, seller_prices])
    writer.writerow([
    driver.current_url,
    title.text,
    brand.text,
    description.text,
    (price.text).replace('Prix moyen : ', ''),
    img.get_attribute("src"),
    sellers,
    seller_prices
    ])

def cycle_through_pagination():
    while True:
    # PRODUCT DATA
        urls = driver.find_elements(By.CSS_SELECTOR, '.product')
        for idx, url in enumerate(urls):
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(' + str(idx + 1) + ') > div > div.relative > span')))
            url = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(' + str(idx + 1) + ') > div > div.relative > span')))
            url.click()
            collect_from_product_page()
            driver.back()
        try:
            next_page = driver.find_element(By.XPATH, "//*[text()='»']").get_attribute('href')
            driver.get(next_page)
        except:
            break

def cycle_through_categories():
    categories = driver.find_elements(By.CSS_SELECTOR, '.menuparapharmacie > div > ul > li > a')
    print(categories)
    categories_url = []

    for category in categories:
        categories_url.append(category.get_attribute('href'))
    for category_url in categories_url:
        driver.get(category_url)
        print(driver.current_url)


# Set up the web driver (e.g. Chrome)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)
driver.get("https://www.pharmanity.com/parapharmacie/materiel-medical-p5")


# Navigate to the web page
# driver.get("https://www.pharmanity.com/parapharmacie/complements-alimentaires-p63")
# https://www.pharmanity.com/parapharmacie/huile-essentielle-bergamote-bio-10-ml-prd409312
# https://www.pharmanity.com/parapharmacie/dermatologie-p64
# https://www.pharmanity.com/parapharmacie

# Wait for the page to load completely
wait = WebDriverWait(driver, 50)
cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allowGoogleAnalytics"]')))

# Click on the accept button
cookie_button.click()

cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save-btn"]')))
cookie_button.click()

# create the csv writer
with open('export_data.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_url','product_name', 'brand', 'description', 'mean_price', 'img_url', 'sellers', 'seller_prices'])
    cycle_through_pagination()

# Close the web driver
driver.quit()
