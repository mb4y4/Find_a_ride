from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
    /537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def get_basic_info(content_list):
    basic_info = []
    for item in content_list:
        basic_info.append(item.find_all('div', attrs={'class': 'masonry-wall.b-list-advert_gallery'}))
    return basic_info


def get_names(basic_info):
    names = []
    for item in basic_info:
        for i in item:
            try:
                names.append(i.find_all("h1", attrs={"class": "b-advert-title-inner qa-advert-title b-advert-title-inner--h1"})[0].text.strip())
            except IndexError:
                names.append(None)
    return names


def get_prices(basic_info):
    prices = []
    for item in basic_info:
        for i in item:
            prices.append(i.find_all("div", attrs={"class": "qa-advert-price-view b-alt-advert-price__container"})[0].string.replace(u'\xa0', u' ').strip())
    return prices


def get_years(basic_info):
    years = []
    for item in basic_info:
        for i in item:
            years.append(i.find_all("h3", attrs={"class": "b-advert-attribute__value"})[0].text.strip())
    return years


def get_motor(basic_info):
    tables = []
    motors = []
    mileages = []
    data = [motors, mileages]
    for item in basic_info:
        for i in item:
            tables.append(i.find_all("div", attrs={"class": "qa-advert-item b-advert-card"})[0])
    for table in tables:
        motors.append(table.find("div", attrs={"class": "b-advert-attribute_value"}).string)
        mileages.append(table.find("span", attrs={"itemprop": "milageFromOdometer"}).string)
    return data


names = []
prices = []
years = []
motors = []
mileages = []

for i in range(9):
    base_url = "https://jiji.co.ke/cars"
    response = get(base_url, headers=headers)
    
if response.status_code == 200:
    html_soup = BeautifulSoup(response.text, 'html.parser')
    car_links = html_soup.find_all('div', class_='masonry-item')

    basic_info = get_basic_info(car_links)
    names1 = get_names(basic_info)
    prices1 = get_prices(basic_info)
    years1 = get_years(basic_info)
    motors1 = get_motor(basic_info)[0]
    mileages1 = get_motor(basic_info)[1]

    #print(f"Car Links: {car_links}")
    print(f"Names: {names1}")
    print(f"Prices: {prices1}")
    print(f"Years: {years1}")
    print(f"Motors: {motors1}")
    print(f"Mileages: {mileages1}")

    names.extend(names1)
    prices.extend(prices1)
    years.extend(years1)
    motors.extend(motors1)
    mileages.extend(mileages1)
    time.sleep(random.randint(1, 2))

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


cols = ["Name", "Year", "Motor", "Mileage (Km)", "Price"]
data = pd.DataFrame({"Name": names, "Year": years, "Motor": motors, "Mileage (Km)": mileages, "Price": prices})[cols]
data["Price"] = data["Price"].replace({'\\$ ': ''}, regex=True)
data["Price"] = data["Price"].replace({'\\,': ''}, regex=True)
data["Mileage (Km)"] = data["Mileage (Km)"].replace({'\\ Km': ''}, regex=True)
data[["Mileage (Km)", "Year", "Motor", "Price"]] = data[["Mileage (Km)", "Year", "Motor", "Price"]].apply(pd.to_numeric)

data.head()
print(data.head())
print(len(data))    

#data.drop_duplicates().to_excel('Car_list.xlsx', index=False)

