from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

def scrape_branch_info():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.google.com/maps/search/Scotiabank+in+Toronto/@43.637422,-79.4901441,13z/data=!3m1!4b1?entry=ttu"
    driver.get(url)
    time.sleep(5)  

    branches = []
    try:
        # Scroll to load all elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Click into each branch to extract details
        results = driver.find_elements(By.CLASS_NAME, 'section-result')
        for result in results:
            result.click()
            time.sleep(2)  # Allow time for branch details to load

            name = driver.find_element(By.CLASS_NAME, 'section-hero-header-title-title').text
            address = driver.find_element(By.CLASS_NAME, 'section-info-text').text
            rating = driver.find_element(By.CLASS_NAME, 'section-star-display').text
            reviews = [review.text for review in driver.find_elements(By.CLASS_NAME, 'section-review-text')]

            branches.append((name, address, rating, ','.join(reviews)))
            driver.back()
            time.sleep(2)  # Wait before the next loop iteration

    finally:
        driver.quit()
    return branches

#save to sql
def save_to_sqlite(data):
    conn = sqlite3.connect('scotiabank_branches.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            name TEXT,
            address TEXT,
            rating TEXT,
            reviews TEXT
        )
    ''')
    c.executemany('INSERT INTO branches (name, address, rating, reviews) VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

branch_data = scrape_branch_info()
save_to_sqlite(branch_data)
