import requests
import time
import csv
from lxml import html


import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
]


def get_text(element):
    return element.text_content().strip() if element is not None else ""

def scrape_flipkart_to_csv(num_pages, output_file):
    headers = {
    "User-Agent": random.choice(user_agents)
    }

    all_data = []

    for page in range(1, num_pages + 1): #pagenation

        url = f"https://www.flipkart.com/search?q=footwear&page={page}"
        
        r = requests.get(url, headers=headers)
        
        tree = html.fromstring(r.content)
        items = tree.xpath('//div[contains(@class,"_1sdMkc LFEi7Z")]')
          

        for index, item in enumerate(items):
            
            link_tag = item.xpath('.//a[contains(@href, "/p/")]')
            product_link = "https://www.flipkart.com" + link_tag[0].get("href") if link_tag else "N/A"

            brand_tag = item.xpath('.//div[contains(@class,"syl9yP")]')
            brand = get_text(brand_tag[0]) if brand_tag else "N/A"

            price_tag = item.xpath('.//div[contains(@class,"Nx9bqj")]')
            original_price_tag = item.xpath('.//div[contains(@class,"yRaY8j")]')
            discount_tag = item.xpath('.//div[contains(@class,"UkUFwK")]')

            price = get_text(price_tag[0]) if price_tag else "N/A"
            original_price = get_text(original_price_tag[0]) if original_price_tag else "N/A"
            discount = get_text(discount_tag[0]) if discount_tag else "N/A"
            
            all_data.append([
                brand, product_link, price, original_price, discount
            ])

        time.sleep(1.5)

    # Write to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Brand", "Product Link", "Price", "Original Price", "Discount"])
            writer.writerows(all_data)
# Run test
scrape_flipkart_to_csv(10, 'shoes.csv')
