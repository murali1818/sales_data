import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Generate random User-Agent to avoid bot detection
ua = UserAgent()

# Function to get product prices from Flipkart
def get_flipkart_prices(product_name):
    headers = {"User-Agent": ua.random}
    search_url = f"https://www.flipkart.com/search?q={product_name}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find_all('div', {'class': '_30jeq3'})

        prices = [float(price.text.replace('₹', '').replace(',', '').strip()) for price in price_elements]
        return sorted(prices) if prices else None
    else:
        print(f"Flipkart request failed. Status Code: {response.status_code}")
        return None

# Function to get product prices from Amazon
def get_amazon_prices(product_name):
    headers = {"User-Agent": ua.random}
    search_url = f"https://www.amazon.in/s?k={product_name}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find_all('span', {'class': 'a-price-whole'})

        prices = [float(price.text.replace(',', '').strip()) for price in price_elements]
        return sorted(prices) if prices else None
    else:
        print(f"Amazon request failed. Status Code: {response.status_code}")
        return None

# Function to get product prices from Reliance Digital
def get_reliance_prices(product_name):
    headers = {"User-Agent": ua.random}
    search_url = f"https://www.reliancedigital.in/search?q={product_name}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find_all('span', {'class': 'TextWeb__Text-sc-1cyx778-0'})

        prices = [float(price.text.replace('₹', '').replace(',', '').strip()) for price in price_elements if '₹' in price.text]
        return sorted(prices) if prices else None
    else:
        print(f"Reliance Digital request failed. Status Code: {response.status_code}")
        return None

# Function to get prices from all websites
def get_all_prices(product_name):
    websites = {
        "Flipkart": get_flipkart_prices(product_name),
        "Amazon": get_amazon_prices(product_name),
        "Reliance Digital": get_reliance_prices(product_name),
    }

    for site, prices in websites.items():
        if prices:
            print(f"\n{site} Prices:")
            for price in prices:
                print(f"₹{price}")
        else:
            print(f"\nNo prices found on {site}.")

# Example Usage
product_name = input("Enter the product name: ")
get_all_prices(product_name)
