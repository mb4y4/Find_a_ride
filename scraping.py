from bs4 import BeautifulSoup
import requests

base_url = "https://jiji.co.ke/vehicles"
response = requests.get(base_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Find all anchor elements that contain information about cars
    car_links = html_soup.find_all('div', class_='b-list-advert__gallery__item js-advert-list-item')

    # Create a new file to store information about cars
    with open('car_information.txt', 'w', encoding='utf-8') as file:
        # Loop through each car link and extract relevant information
        for car_link in car_links:
            # Extract information (modify this based on the actual HTML structure)
            car_name_element = car_link.find('div', class_='b-advert-title-inner qa-advert-title b-advert-title-inner--div')
            car_price_element = car_link.find('div', class_='qa-advert-price')

            if car_name_element and car_price_element:
                car_name = car_name_element.text.strip()
                car_price = car_price_element.text.strip()

                # Write information to the file
                file.write(f"Car Name: {car_name}\nPrice: {car_price}\n\n")

    print("Data has been successfully written to 'car_information.txt'")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
