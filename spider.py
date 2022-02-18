from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
                    NoSuchElementException,
                    StaleElementReferenceException,
                    TimeoutException,
                )
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, asyncio
import re
from typing import Any, Callable, Dict, Iterable, Tuple
import logging
import xlsxwriter



logger = logging
logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR, filename='logs.txt')


NewsOutPut = list[Any]
SlugsOutPut = list[Any]


def parse_content(content_list):

    content_merge = " ".join(content_list)

    content = re.sub('<[^>]+>', '', content_merge)

    return content


def parse_single_content(content):


    content = re.sub('<[^>]+>', '',content)

    return content





class CompanySpider(webdriver.Chrome):


    def __init__(self, driver_path='', teardown=False):
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-infobars")
        options.add_argument('--disable-popup-blocking')
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--disable-gpu')
        super(CompanySpider, self).__init__(options=options)
        self.implicitly_wait(6)
        self.maximize_window()
        self.alphabets = [
                'A',
                'B',
                'C',
                'D',
                'E',
                'F',
                'G',
                'H',
                'I',
                'J',
                'K',
                'L',
                'M',
                'N',
                'O',
                'P',
                'Q',
                'R',
                'S',
                'T',
                'U',
                'V',
                'W',
                'X',
                'Y',
                'Z'

        ]


    def parse_table_rows(self, rowdata_elements):

        all_data = []

        for element in rowdata_elements:
            row_elements = element.find_elements(
                                        By.TAG_NAME,
                                        'td'
                                )
            sd = []
            for elem in row_elements:
                data = elem.get_attribute('innerHTML')
                pd = parse_single_content(data)
                sd.append(pd)
            all_data.append(sd)

        wanted_list = all_data[1:]

        required_data = []

        for data in wanted_list:
            name = data[0]
            dob = data[1]
            location = data[2]

            required_data.append(

                {

                    'name': name,
                    'dob': dob,
                    'location': location
                }

            )

        return required_data
        



    def get_entire_data_pages(self, rowdata_elements):

        data = []

        first_page_data = self.parse_table_rows(rowdata_elements)

        for dt in first_page_data:
            data.append(dt)

        next_button_avaliable = True

        while next_button_avaliable:

            try:
                button_element = self.find_element(
                                By.XPATH,
                                "//*[@id='next-page']"
                    )

                try:
                    self.execute_script("arguments[0].click();", button_element)

                    table_element = self.find_element(
                                        By.XPATH,
                                        "//*[contains(@class, 'full-width-table')]"
                                    )
                    rowdata_elements = table_element.find_elements(
                                                            By.TAG_NAME,
                                                            'tr'
                                                    )
                    page_data = self.parse_table_rows(rowdata_elements)

                    for dt in page_data:
                        data.append(dt)
                except:
                    pass

            except NoSuchElementException:
                print('Button Lapsed')
                next_button_avaliable = False

        print(data)
        print(len(data))

        return data









    def scrape_alphabet_details(self, alphabet):
        url = "https://find-and-update.company-information.service.gov.uk/register-of-disqualifications/"
        


        qualified_url = f"{url}{alphabet}"

        data = []
        self.get(qualified_url)
        try:
            table_element = self.find_element(
                                    By.XPATH,
                                    "//*[contains(@class, 'full-width-table')]"
                                )
            rowdata_elements = table_element.find_elements(
                                                    By.TAG_NAME,
                                                    'tr'
                                                )

            data = self.get_entire_data_pages(rowdata_elements)
        except NoSuchElementException:
            print('Table not found')


        return data
        






    def scrape_companies(self):
        workbook = xlsxwriter.Workbook('companies.xlsx')
        print(workbook)
        for letter in self.alphabets[0:2]:
            data = self.scrape_alphabet_details(letter)       
            work_sheet = workbook.add_worksheet(letter)
            work_sheet.write('A1', 'NAME')
            work_sheet.write('B1', 'DATE OF BIRTH')
            work_sheet.write('C1', 'LOCATION')
            row_index = 1
            for d in data:
                work_sheet.write('A'+ str(row_index), d['name'])
                work_sheet.write('B'+ str(row_index), d['dob'])
                work_sheet.write('C'+ str(row_index), d['location'])
                row_index += 1

        workbook.close()


        self.quit()









