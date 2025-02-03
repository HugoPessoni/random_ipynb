import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyautogui as pa
from selenium.common.exceptions import NoSuchElementException


URL = 'https://www.tripadvisor.com.br/Restaurant_Review-g303324-d11890472-Reviews-Best_Burger-Goiania_State_of_Goias.html#REVIEWS'

def get_data(driver):
    print('get data...')
    
    #more_elements = driver.find_elements(By.CLASS_NAME, 'w8nwRe')
    #more_elements = 10
    #for element in more_elements:
    #    element.click()
    
    elements = driver.find_elements(By.CLASS_NAME, 'rev_wrap ui_columns is-multiline')
    lst_data = []
    
    for data in elements:
        #name = data.find_element(By.CSS_SELECTOR, '.d4r55').text
        #date = data.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        #text = data.find_element(By.CSS_SELECTOR, '.wiI7pd').text
        #score = data.find_element(By.CSS_SELECTOR, '.kvMYJc').get_attribute("aria-label")
        try:
            name = data.find_element(By.CSS_SELECTOR, '.d4r55').text
        except NoSuchElementException:
            name = None  # Ou algum valor padrão

        try:
            date = data.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        except NoSuchElementException:
            date = None  # Ou algum valor padrão

        try:
            text = data.find_element(By.CSS_SELECTOR, '.MyEned .wiI7pd').text
        except NoSuchElementException:
            text = None  # Ou algum valor padrão

        try:
            score_element = data.find_element(By.CSS_SELECTOR, '.kvMYJc')
            score = score_element.get_attribute("aria-label")
        except NoSuchElementException:
            score = None  # Ou algum valor padrão

        lst_data.append([name, date, text, score])
    return lst_data

def counter(driver):
    result_element = driver.find_element(By.CLASS_NAME, 'reviews_header_count')
    result_text = result_element.text  # Este é o texto, por exemplo "(35)"
    result_number = result_text.strip('()')  # Remove os parênteses, deixando apenas "35"
    #result_number = int(result_text.split(' ')[0].replace(',', ''))
    #return int(result_number / 10) + (result_number % 10 > 0) + 3
    return result_number

    # fazer um counter de quantas paginas possui

'''def scrolling(driver, count): #teste falho
    print('scrolling...')
    #scrollable_element = driver.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf ')
    #actions = ActionChains(driver)
    for _ in range(count):
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #element = driver.find_element(By.TAG_NAME,"m6QErb DxyBCb kA9KIf dS8AEf ")
        #element.send_keys(Keys.PAGE_DOWN)
        #actions.move_to_element(scrollable_element).click().send_keys("PAGE_DOWN").perform()
        time.sleep(3)'''

'''def scrolling(counter):
    print('scrolling...')
    scrollable_div = driver.find_element(By.CLASS_NAME,
        'm6QErb DxyBCb kA9KIf dS8AEf ')
    for _i in range(counter):
        scrolling = driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight', 
            scrollable_div
        )
        time.sleep(3)'''

'''def scrolling(driver):
    try:
        # Aguarde até que o primeiro elemento da classe seja carregado
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'jftiEf fontBodyMedium'))
        WebDriverWait(driver, 10).until(element_present)

        # Enquanto existirem elementos a serem carregados
        while True:
            # Tente rolar até o final do elemento
            driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jftiEf fontBodyMedium'))))

            # Aguarde para carregar mais elementos (ajuste o tempo conforme necessário)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jftiEf fontBodyMedium')))
    except TimeoutException:
        print("Timed out waiting for page to load")'''

'''def scroll_to_load_reviews(driver, timeout=3, max_scrolls=10):
    # Localizar o elemento que contém as avaliações
    scrollable_div = driver.find_element(By.XPATH,'//div[@class="lXJj5c Hk4XGb"]')
    
    # Realizar o scroll um número específico de vezes
    for _ in range(max_scrolls):
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight;', 
            scrollable_div
        )
        # Aguardar para que o conteúdo seja carregado
        time.sleep(timeout)'''

'''def scrolling(counter):
    pa.moveTo(769, 614)
    for x in range(counter*2):
       pa.scroll(-1000) 
       time.sleep(0.5)
    return print('scrolling done')'''

'''def write_to_xlsx(data):
    print('write to excel...')
    cols = ["Nome", "Data", "Titulo", "Comentário", "Avaliação" ]
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('out.xlsx')'''

if __name__ == "__main__":
    print('starting...')
    options = Options()
    options.add_argument("--lang=en-US")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(10)
    #content = driver.page_source
    #soup = BeautifulSoup(content, features='html.parser')

    counter = counter(driver)
    print(counter)
    #scrolling(counter)
    #data = get_data(driver)
    #driver.close()

    #write_to_xlsx(data)
    print('Done!')
