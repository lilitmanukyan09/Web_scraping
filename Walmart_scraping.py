#importing necessary libraries

import time
from selenium import webdriver
from scrapy.http import TextResponse
import pandas as pd

#URL and cities to scrape
url_walmart = 'https://www.walmart.ca/en/stores-near-me'
cities = ['Vancouver', 'Edmonton', 'Calgary', 'Saskatoon', 'Regina', 'Ottawa', 'Toronto']

#Adding options for the Google Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Opening a browser window
browser = webdriver.Chrome(options=options)
browser.maximize_window()

#Creating an empty list to store the scraped information
address_walmart = []
#Iterating over all the cities
for c in cities:
    for i in range(1, 20):
        try:
            page = browser.get(url_walmart)
            # Applying a time delay for allowing the page to load completely
            time.sleep(2)
            browser.find_element_by_class_name('sfa-search__input').click()
            # Applying a time delay for allowing the page to load completely
            time.sleep(2)
            city = c
            browser.find_element_by_class_name('sfa-search__input').clear()
            browser.find_element_by_class_name('sfa-search__input').click()
            browser.find_element_by_class_name('sfa-search__input').send_keys(city)
            browser.find_element_by_class_name('sfa-store-list-item__name').click() 
            page = browser.page_source
            response = TextResponse(url=url_walmart,body=page,encoding ="utf-8")
            # Applying a time delay for allowing the page to load completely
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[4]/div[2]/div/div[2]/div/div['+ str(i) + ']/div[2]/h2').click() 
            response = TextResponse(url=url_walmart,body=page,encoding ="utf-8")
            #Extracting and appending the address to the list
            address_walmart.append(response.xpath('//*[@id="skipto-main-wrap"]/div/div[4]/div[4]/div/div[2]/div[1]/div[1]/div/div//text()').getall())
            print(address_walmart)
        except:
            pass
#Exporting the output dataframe as an xlsx file
pd.DataFrame(address_walmart).to_excel("Walmart.xlsx")
print(address_walmart)