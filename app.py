
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from openpyxl import Workbook
import pandas as pd

#from env import URL, DriverLocation

URL = 'https://www.google.com.br/maps/place/Novo+Mundo+-+Inhumas+-+Filial+07/@-16.3600341,-49.5037273,17z/data=!4m11!1m2!2m1!1smoveis!3m7!1s0x935e7868c89152e9:0xd148493058f690ac!8m2!3d-16.3600341!4d-49.4993499!9m1!1b1!16s%2Fg%2F1q5gn5k4p?entry=ttu'
DriverLocation = "./Driver/chromedriver.exe"

def get_data(driver):
    """
    this function get main text, score, name
    """
    print('get data...')
    more_elemets = driver.find_elements_by_class_name('w8nwRe kyuRq') #CLASSE DO BOTÃO "MAIS"
    for list_more_element in more_elemets:
        list_more_element.click()
    
    elements = driver.find_elements_by_class_name(
        'jftiEf')
    lst_data = []
    for data in elements:
        name = data.find_element_by_xpath(
            './/a/div[@class="d4r55"]/span').text
        text = data.find_element_by_xpath(
            './/div[@class="MyEned"]/span[2]').text
        score = data.find_element_by_xpath(
            './/span[@class="kvMYJc"]').get_attribute("aria-label")

        lst_data.append([name, text, score[1]])

    return lst_data


def counter():
    result = driver.find_element_by_class_name('jANrlb').find_element_by_class_name('fontBodySmall').text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(int(result[0])/10)+1


def scrolling(counter):
    print('scrolling...')
    scrollable_div = driver.find_element_by_xpath(
        '//div[@class="lXJj5c Hk4XGb"]')
    for _i in range(counter):
        scrolling = driver.execute_script(
            'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
            scrollable_div
        )
        time.sleep(3)


def write_to_xlsx(data):
    print('write to excel...')
    cols = ["name", "comment", 'rating']
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('out.xlsx')


if __name__ == "__main__":

    print('starting...')
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # show browser or not
    options.add_argument("--lang=en-US")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    DriverPath = DriverLocation
    driver = webdriver.Chrome(service=Service(DriverPath), options=options)

    driver.get(URL)
    time.sleep(5)

    counter = counter()
    scrolling(counter)

    data = get_data(driver)
    driver.close()

    write_to_xlsx(data)
    print('Done!')
