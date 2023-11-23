'''
    This is just a copy of your work, but with some other optimizations to keep the data clean and easily reachable
    I've made this so I can only modify this file instead of tampering with yours.
    I'll be adding in more items, feel free to pick any concept or functionality from here
    Remember to delete this file/folder after all work is done for presentations on Saturday
'''

from bs4 import BeautifulSoup
import requests
import sqlite3
import re

connection = sqlite3.connect('info.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS cars_info')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars_info(
               id INT PRIMARY KEY NOT NULL,
               name TEXT NOT NULL,
               price_ksh INT NOT NULL
    )
''')


base_url = "https://jiji.co.ke/cars"


def get_website_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return f'The website get request is not ok. status {response.status_code}'


def clean_prices(price):
    pattern = r'[0-9 \,]'
    cleaned = re.findall(pattern, price)
    results = ''.join(cleaned)
    return results


def fetch_cars():
    response = get_website_response(base_url)
    html_soup = BeautifulSoup(response, 'html.parser')

    car_links = html_soup.find_all('div', class_='masonry-item')
    i = 0
    for car in car_links:
        i += 1
        car_name = car.find('div', class_='b-advert-title-inner').text
        car_price_unclean = car.find('div', class_='qa-advert-price').text
        car_price = clean_prices(car_price_unclean)

        cursor.execute('INSERT INTO cars_info VALUES (?,?,?)', (i, car_name, car_price))
        connection.commit()



fetch_cars()        
cursor.close()

