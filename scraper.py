from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json

def scrape_yelp():
    # Set up Chrome options
    options = Options()
    options.headless = True  # Running in headless mode
    driver = webdriver.Chrome(options=options)

    branches_data = []  # List to store data dictionaries

    try:
        # Navigate to Yelp's search page
        driver.get("https://www.yelp.com/search?find_desc=Scotiabank&find_loc=Toronto")
        time.sleep(5)  # Wait for the page to load

        # Extract data
        branches = driver.find_elements(By.CSS_SELECTOR, "div.container__09f24__sxa9- div.mainAttributes__09f24__26-vh")
        for branch in branches:
            name = branch.find_element(By.CSS_SELECTOR, "a.link__09f24__1kwXV").text
            rating = branch.find_element(By.CSS_SELECTOR, "div.i-stars__09f24__M1AR7").get_attribute('aria-label')
            branches_data.append({"Name": name, "Rating": rating})
            print(f"Name: {name}, Rating: {rating}")

    finally:
        driver.quit()

    # Write data to a JSON file
    with open('yelp_scotia_data.json', 'w') as json_file:
        json.dump(branches_data, json_file, indent=4)

scrape_yelp()