import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pyautogui as pa
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os
from bs4 import BeautifulSoup
from typing import List
from selenium.webdriver.common.keys import Keys



class Maps_Scraper:
    def __init__(self, url: str, no_inteface: bool = False):
        self.url = url
        self.driver = self._driver_init(no_inteface)

    @staticmethod
    def _driver_init(no_inteface: bool):
        # Obter path do executável do Chrome e do ChromeDriver
        chrome_path = os.getenv('CHROME_PATH')
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')

        if not chrome_path: 
            raise ValueError('CHROME_PATH is not defined')
        if not chromedriver_path:
            raise ValueError('CHROMEDRIVER_PATH is not defined')

        # Incializalização de driver
        chrome_options = Options()
        chrome_options.binary_location = chrome_path

        # Modo sem interface gráfica para rodar em servidores
        if no_inteface:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--window-size=1920x1080")

        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver

    def get_data(self):
        print('get data...')
        all_dicts = []

        # Clicar para mostrar as avaliações
        elemento = self.driver.find_element(By.XPATH, "//div[@class='Gpq6kf fontTitleSmall' and text()='Avaliações']")
        elemento.click()

        # Scrollar para carregar todos os comentários
        self.scrolling()

        more_elements = self.driver.find_elements(By.CLASS_NAME, 'w8nwRe')
        for element in more_elements:
            element.click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')  

        div = soup.find('div', class_='m6QErb DxyBCb kA9KIf dS8AEf XiKgde')
        comments = div.find_all('div', class_='jJc9Ad')

        for comment in comments: 
            comment_dict = {}
            comment_dict['text'] = comment.find('span', class_='wiI7pd').text
            comment_dict['score'] = comment.find('span', class_='kvMYJc').get('aria-label')
            comment_dict['name'] = comment.find('div', class_='d4r55').text
            comment_dict['relative_date'] = comment.find('span', class_='rsqaWe').text 
            all_dicts.append(comment_dict)

        return all_dicts
    
    def get_number_reviews(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')  

        div = soup.find('div', class_='m6QErb DxyBCb kA9KIf dS8AEf XiKgde')
        comments = div.find_all('div', class_='jJc9Ad')

        return len(comments)
    
    def save_to_csv(self, data: List[dict]):
        df = pd.DataFrame(data)
        df.to_csv('out.csv', index=False)
        
    def counter(self):
        result_text = self.driver.find_element(By.CLASS_NAME, 'jANrlb').find_element(By.CLASS_NAME, 'fontBodySmall').text
        result_number = int(result_text.split(' ')[0].replace(',', ''))
        return result_number

    def scrolling(self):
        total_reviews = 340
        n_reviews = 0

        container = self.driver.find_element(By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]")

        while n_reviews < total_reviews:
            self.driver.execute_script("arguments[0].scrollBy(0, 2000);", container)
            n_reviews = self.get_number_reviews()
            print(n_reviews)
            time.sleep(0.8)

        return print('scrolling done')
    
    def start_scrap(self):
        self.driver.get(self.url)
        time.sleep(2)
        data = self.get_data()
        self.save_to_csv(data)
        self.driver.close()
        print('Done!')


if __name__ == "__main__":
    URL = \
    """
    https://www.google.com/maps/place/Bianco+Ristorante/data=!4m7!3m6!1s0x935efb0c9f1c4f21:0xfac8d868d02056ae!8m2!3d-16.6967677!4d-49.2603075!16s%2Fg%2F11rwp80b4c!19sChIJIU8cnwz7XpMRrlYg0GjYyPo?authuser=0&hl=pt-BR&rclk=1
    """
    
    scraper = Maps_Scraper(url=URL)
    scraper.start_scrap()
    