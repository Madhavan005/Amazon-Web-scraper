"""
                    AMAZON WEB SCRAPER

Title: Amazon web scraper
description: Search products in Amazon website and extract data of each product then stored in JSON file
Author: Gyana Madhavan C

"""


from bs4 import BeautifulSoup
import requests
import json
import concurrent.futures
import time

print("              Welcome to Amazon Web Scarper             ")
print("*"*60)
json_dict = {}
products = {}

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# Search in amazon website
def Search():
    amazon_url = "https://www.amazon.in/s?k="
    user_input = input("Enter the product name:").strip()
    key = user_input.replace(" ", "+")
    f_url =f"{amazon_url}{key}"
    return f_url, user_input
url, product_name = Search()


content = requests.get(url, headers =HEADERS)
soup = BeautifulSoup(content.text, 'lxml')
print(f"Search result for product {product_name} is found! ")
links = []
for post in soup.find_all(cel_widget_id="MAIN-SEARCH_RESULTS"):
    # print(i.a["href"])
    li = f"https://www.amazon.in{post.a['href']}"
    links.append(li)

if len(links) == 0:
    print("noting found!")
else:
    print(f"Total number of product found is {len(links)}")





def extracter(page, count):
    # count = 1
    content = requests.get(page, headers=HEADERS)
    soup = BeautifulSoup(content.text, 'html.parser')

    # product title
    try:
        title = soup.find(id='productTitle').get_text().strip()

        products['Title'] = title
    except:
        products['Title'] = ''
    # product Image
    try:
        img_ = soup.find('div', class_='imgTagWrapper')
        imgs_str = img_.img.get('data-a-dynamic-image')

        # convert to a dictionary
        imgs_dict = json.loads(imgs_str)

        # each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
        first_link = list(imgs_dict.keys())[0]
        products['Image'] = first_link
    except:
        products['Image'] =''

    # product rating
    try:
        star = soup.find('a', class_ ="a-popover-trigger a-declarative").get_text().strip()
        products['Rating'] = star
    except:
        products['Rating'] = '0 out of 5 stars'

    # product price
    try:
        price = soup.find(id='priceblock_ourprice').get_text().replace('₹', '').strip()
        products['Price'] = price
    except:
        products['Price'] = ''

    # product delivery date
    try:
        delivery =soup.find(id="ddmDeliveryMessage" ).b.get_text().strip()
        products['Delivery date'] = delivery
    except:
        products['Delivery date'] = ''

    # product availablity
    try:
        avail = soup.find(id="availability" ).text.strip()
        products['Availability'] = avail
    except:
        products['Availability'] =''

    json_dict[count]=products

    # Writing
    json_filename = f"{product_name}.json"
    with open(json_filename, 'w') as jfile:
        json.dump(json_dict, jfile, indent=4, sort_keys=True)


def Main():

    start = time.perf_counter()

    print("Extracting Product details..")
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        count = [x for x in range(len(links)+1)]
        executor.map(extracter, links, count)

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} sec")
    print(f"Product details are stored in {product_name} JSON file")


if __name__ == '__main__':
    Main()
