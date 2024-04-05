from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notifypy import Notify
import os
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["amazon"]
collection = db["prices"]


def notify():
    notification = Notify()
    notification.title = "Extracting Data..."
    notification.message = "Extracting data from Amaozn"
    notification.send()

def get_data():
    options = Options()
    options.add_argument("--headless") # it will not show that fetching data from browser
    #user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    with open("products.txt") as f:
        products = f.readlines()
    driver = webdriver.Chrome(options=options)

    for product in products:
        driver.get(f"https://www.amazon.in/dp/{product}")
        page_source = driver.page_source
        with open(f"data/{product.strip()}.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
        
def extract_data():
    files = os.listdir("data")
    for file in files:
        #print(file)
        with open(f"data/{file}", encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.getText().split(":")[0]
        time = datetime.now()
        #print(soup.title)
        
        priceTxt = soup.find(class_="a-price-whole")
        price = priceTxt.getText().replace(".", "").replace(" ", "").replace(",", "")
        table = soup.find(id="productDetails_detailBullets_sections1")
        asin = table.find(class_="prodDetAttrValue").getText().strip()
        print(price, asin, time)
        
        collection.insert_one({"price": price, "asin": asin, "title": title, "time": time})
        
        # with open("finaldata.txt", "a") as f:
        #     f.write(f"{price}~~{asin}~~{title}~~{time}\n")
        
        
    

if __name__ == "__main__":
    # notify()
    
    # to get data from the provided products link
    # get_data()
    
    extract_data()
