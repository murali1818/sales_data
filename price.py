import time
import requests
from bs4 import BeautifulSoup

def get_all_prices(product_name, retries=3):
    search_url = f"https://www.flipkart.com/search?q={product_name}"

    for _ in range(retries):
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all the prices on the page
            price_elements = soup.find_all('div', {'class': '_1vC4OE'}) + soup.find_all('div', {'class': '_30jeq3'})

            if price_elements:
                prices = [float(price.text.replace('₹', '').replace(',', '').strip()) for price in price_elements]

                if prices:
                    return sorted(prices)
                else:
                    print("Prices not found on the page.")
                    return None
            else:
                print("No price elements found on the page.")
                return None

        elif response.status_code == 503:
            print("Server is currently unavailable. Retrying...")
            time.sleep(5)  # Add a delay of 5 seconds before retrying
            continue

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")
            return None

    print(f"Unable to retrieve prices for {product_name} on Flipkart after {retries} retries.")
    return None

# Example usage:
product_name = input("Enter the product name: ")
all_prices = get_all_prices(product_name)

if all_prices is not None:
    print(f"All prices for {product_name} on Flipkart in ascending order are:")
    for price in all_prices:
        print(f"₹{price}")
else:
    print(f"Unable to retrieve prices for {product_name} on Flipkart.")
