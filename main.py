from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
import os

# Initialize the WebDriver (you can choose the appropriate webdriver for your browser)
driver = webdriver.Chrome()

def random_delay(min, max):
    delay_time = random.uniform(min, max)
    time.sleep(delay_time)

def getRviewpage():

    reviewxpath = '*//div[@class="a-section review aok-relative"]'
    nameXpath = './/span[@class="a-profile-name"]'
    rtitle = './/span[@class="a-letter-space"]/following-sibling::span[1]'
    rdate = './/div/span[@data-hook="review-date"]'
    review = './/div/span[@data-hook="review-body"]'

    # Wait for review data to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, reviewxpath)))
    random_delay(3,5)
    reviewdata = driver.find_elements(By.XPATH, reviewxpath)
    print(reviewdata)
    data_list = []

    for i in reviewdata:
        i = WebDriverWait(driver, 10).until(EC.visibility_of(i))


        
        name = i.find_element(By.XPATH, nameXpath).text
        title = i.find_element(By.XPATH, rtitle).text
        date_location = i.find_element(By.XPATH, rdate).text
        review_text = i.find_element(By.XPATH, review).text

        data_list.append({
            'Name': name,
            'Title': title,
            'Date and Location': date_location,
            'Review': review_text
        })

    df = pd.DataFrame(data_list)
    return df

def getdata(url):
    driver.get(url)
    
    # Wait for "See more reviews" link to be clickable
    see_more_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "*//a[contains(text(), 'See more reviews')]"))
    )
    see_more_link.click()

    # Set the number of pages you want to scrape
    pages_to_scrape = 5

    for page in range(1, pages_to_scrape + 1):
        df = getRviewpage()
        df['URL'] = url
        print(df)
        
        try:
            file_name = 'reviews_data.csv'
            if os.path.isfile(file_name):
                existing_data = pd.read_csv(file_name)
                df = pd.concat([existing_data, df], ignore_index=True)
        except Exception as e:
            print(f"Error: {e}")

        df.to_csv(file_name, index=False)  # Write to CSV outside the try block

        random_delay(2, 3)
        
        # Click next page
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']/a"))
            )
            next_page_button.click()
        except:
            break

def runScrapper():
    driver.get("https://www.amazon.in/")
    productName= "mobile"
    driver.find_element(By.XPATH, '*//input[@placeholder="Search Amazon.in"]').send_keys(productName)
    driver.find_element(By.XPATH, '*//input[@placeholder="Search Amazon.in"]').send_keys(Keys.ENTER)
    allurl = driver.find_elements(By.XPATH, '*//div[@data-component-type="s-search-result"]//h2/a')
    productUrl=[]
    for i in allurl:
        productUrl.append(i.get_attribute("href"))
    for url in productUrl:
        getdata(url)

runScrapper()
