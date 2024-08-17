#### Libraries ####
# Import libraries here
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#### Predefined Variables ####
# Parameter Settings (adjustable)
category = "Mouse kantor" # You can change this value, as long as it contains alphabetical input and whitespace seperated
no_of_page = 2
scrolls_per_page = 15

# Define Base URL here
category = category.lower().replace(" ", "%20")
url = f"https://www.tokopedia.com/search?st=product&q={category}" # In this case, I use tokopedia
# print(url)

#### Driver initialization ####
# Drivers
driver = webdriver.Chrome()
driver.get(url)

# Temp Data Storing
data = []

#### Processing ####
for i in range(no_of_page): # Number of pages
    # Scrolling mechanism
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#zeus-root")))
    time.sleep(2)

    # Data Loading
    for i in range(scrolls_per_page): # Scrolls per page, depends on local device vh
        driver.execute_script("window.scrollBy(0, 250)")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for item in soup.findAll("div", class_="css-5wh65g"):
        product_name = item.find("span", class_="OWkG6oHwAppMn1hIBsC3pQ==")
        product_price = item.find("div", class_="_8cR53N0JqdRc+mQCckhS0g==")
        rating = item.find("span", class_="nBBbPk9MrELbIUbobepKbQ==")
        toko = item.find("span", class_="X6c-fdwuofj6zGvLKVUaNQ==")

        # Note: Added rating in case there is any similar products, users can choose which store is prefered to purchase the
        # product from. Additionally, we can see if there any correlation between price points and the store (if there is any).

        if product_name and product_price and rating and toko:
            data.append(
                (product_name.text, product_price.text, rating.text, toko.text)
            )

df = pd.DataFrame(data, columns=['product_name', 'product_price', 'product_rating', 'product_store'])
print(df)

driver.close()

#### File Saving ####
# Modify name convention
name_convention = category.replace("%20", "-")

# Save DataFrame to CSV
df.to_csv(f'{name_convention}.csv', index=False)

# Save DataFrame to JSON
df.to_json(f'{name_convention}.json', orient='records')
