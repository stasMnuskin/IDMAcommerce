from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv
from csv import writer
import random
import os

count = 0
print(os.getcwd())
with open('Google Maps/final_data.csv', 'a+', newline='', encoding='utf-8') as f_header:
    csv_header = writer(f_header)
    csv_header.writerow(['Company Name', 'Rating', 'Review Count', 'Category', 'Address', 'Website', 'Search Term'])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    with open('Google Maps/search_term.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                page = browser.new_page()
                search_term = row[0]
                name = []
                rating = []
                review_count = []
                address = []
                website = []
                category = []
                page.goto('https://www.google.com/maps')
                page.fill('xpath=//*[@id="searchboxinput"]', f'{row[0]}')
                time.sleep(1)
                page.click('xpath=//*[@id="searchbox-searchbutton"]', timeout=0)
                time.sleep(3)
                page.mouse.move(0,100)
                while not page.is_visible('span.HlvSq'):
                    count = count + 1
                    if count < 50:
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                        page.mouse.wheel(0,500)
                        time.sleep(random.randint(1,2))
                    else:
                        page.click('xpath=//*[@id="searchbox-searchbutton"]', timeout=0)
                        count = 0
                        time.sleep(3)
                        page.mouse.move(0,100)
                count = 0
                time.sleep(5)
                html = page.inner_html('html')
                soup = BeautifulSoup(html, 'html.parser')
                results  = soup.find('div', class_='m6QErb DxyBCb kA9KIf dS8AEf ecceSd').find_all('div', class_='lI9IFe')
                for result in results:
                    try:
                        name = result.find('div', class_='qBF1Pd fontHeadlineSmall').text.strip()
                    except:
                        pass
                    try:
                        rating = result.find('span', class_='MW4etd').text.strip()
                    except:
                        pass
                    try:
                        review_count = result.find('span', class_='UY7F9').text.strip().replace('(','').replace(')','')
                    except:
                        pass
                    try:
                        category = result.find_all('div', class_='W4Efsd')[2].find_all('span')[2].text.strip()
                    except:
                        pass
                    try:
                        address = result.find_all('div', class_='W4Efsd')[2].find_all('span')[6].text.strip()
                    except:
                        pass
                    try:
                        website = result.find('a', class_='lcr4fd S9kvJb')['href']
                    except:
                        pass

                    data = [name, rating, review_count, category, address, website, search_term]

                    with open('Google Maps/final_data.csv', 'a+', encoding='utf-8', newline='') as f:
                        csv_writer = writer(f)
                        csv_writer.writerow(data)
                        f.close()
                    website = ''
                count+=1    
                page.close()
                
            except:
                continue