import time
import os
import django
import threading
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adidasSaleFinder.settings')
django.setup()
from crawler.models import SaleProduct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from whatsapp.messageSender import send_sale_product_to_user

driver = webdriver.Chrome(executable_path=r'C:\Users\USER\Downloads\chromedriver_win32\chromedriver.exe')


def find_element_percent(driver):
    time.sleep(2.0)
    pop_up = driver.find_element(by=By.CLASS_NAME, value='gl-icon.close___3LPSC')
    pop_up.click()
    time.sleep(1)
    element_xpath_value = "//*[@id='main-content']/div/div[3]/div/div/div/div[1]/div"
    items_page = driver.find_element(by=By.XPATH, value=element_xpath_value)
    item_list = items_page.find_elements(by=By.CLASS_NAME, value="grid-item")

    time.sleep(2.0)
    counter = 0
    result_dict = {}
    for item in item_list:
        item_span = None
        counter += 1
        try:
            item_span_element = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/div/a[2]/div/span")
            item_span = item_span_element.text

        except:
            print('item doesn\'t have span percent tag')

        try:
            if int(item_span[1:3]) >= 25:
                # link_of_product
                link = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/div/a[1]").get_attribute('href')
                # print(link)

                # product_name
                name = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/a/div/p[1]").text
                # print(name)

                # product_price
                price = item.find_element(by=By.XPATH,
                                          value=".//a[@class = 'product-card-content-badges-wrapper___2brrU']/div[2]/div/div[1]").text
                # print(price)

                # product_price_on_sale
                price_on_sale = item.find_element(by=By.XPATH,
                                                  value=".//a[@class = 'product-card-content-badges-wrapper___2brrU']/div[2]/div/div[2]").text
                # print(price_on_sale)
                obj = SaleProduct(link=link, name=name, price=price, price_on_sale=price_on_sale)
                obj.save()
                # list_of_items.append(obj)
                item_dict = {"name": name, "price": price, "price_on_sale": price_on_sale}
                # result_dict_key_counter = result_dict_key_counter + 1
                result_dict[link] = item_dict
                # print(result_dict)
                # print(list_of_items)


        except:
            continue

        if counter % 3 == 0:
            driver.execute_script("arguments[0].scrollIntoView(true);", item)
            time.sleep(1.0)

    else:
        print(result_dict)
        try:
            send_sale_product_to_user()
        except:
            time.sleep(1.5)
            send_sale_product_to_user()
        return result_dict


def run_driver(driver):
    target_url = "https://www.adidas.com.tr/tr/outlet"

    try:
        driver.get(target_url)
        uselessWindows = driver.window_handles
        result = find_element_percent(driver)
        return result

    except TimeoutException:
        print("loading took too much time,try again...")
        time.sleep(2.0)
        driver.get(target_url)


while True:

    run_driver(driver)
    time.sleep(60)





